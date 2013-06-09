from datetime import date, timedelta
from django.utils.encoding import smart_str
from bhp_base_model.models import BaseUuidModel
from bhp_map.exceptions import MapperError


class Mapper(object):

    def __init__(self, *args, **kwargs):
        self._item_model_cls = None
        self._regions = None
        self._sections = None
        self._icons = None
        self._other_icons = None
        self._landmarks = None
        # item_model_cls
        if 'model' in kwargs:
            self.set_item_model_cls(kwargs.get('model'))
        if 'regions' in kwargs:
            self.set_regions(kwargs('regions'))
        if 'sections' in kwargs:
            self.set_regions(kwargs('sections'))
        if 'icons' in kwargs:
            self.set_icons(kwargs('icons'))
        if 'other_icons' in kwargs:
            self.set_other_icons(kwargs('other_icons'))
        if 'landmarks' in kwargs:
            self.set_landmarks(kwargs('landmarks'))

    def __repr__(self):
        try:
            u = unicode(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<%s: %s>' % (self.__class__.__name__, u))

    def set_icons(self, tpl=None):
        if tpl:
            if not issubclass(tpl, (tuple, list)):
                raise MapperError('Icons must an instance of tuple or list')
            self._icons = tpl
        else:
            try:
                self._icons = self.icons
            except:
                pass
        if not self._icons:
            raise MapperError('Attribute \'icons\' may not be None (see _icons) .')

    def get_icons(self):
        if not self._icons:
            self.set_icons()
        return self._icons

    def set_other_icons(self, tpl=None):
        if tpl:
            if not isinstance(tpl, (tuple, list)):
                raise MapperError('Icons must an instance of tuple or list')
            self._other_icons = tpl
        else:
            try:
                self._other_icons = self.other_icons
            except:
                pass
        if not self._other_icons:
            raise MapperError('Attribute \'other_icons\' may not be None (see _other_icons) .')

    def get_other_icons(self):
        if not self._icons:
            self.set_icons()
        return self._icons

    def set_item_model_cls(self, cls=None):
        if cls:
            if not issubclass(cls, BaseUuidModel):
                raise MapperError('Item model class must be a subclass of BaseUuidModel')
            self._item_model_cls = cls
        else:
            try:
                self._item_model_cls = self.model
            except:
                pass
        if not self._item_model_cls:
            raise MapperError('Attribute \'model\' may not be None (see _item_model_cls) .')

    def get_item_model_cls(self):
        if not self._item_model_cls:
            self.set_item_model_cls()
        return self._item_model_cls

    def set_regions(self, tpl=None):
        if tpl:
            if not issubclass(tpl, (tuple, list)):
                raise MapperError('Regions must be a list or choices tuple. Got {0}'.format(tpl))
            self._regions = tpl
        else:
            try:
                self._regions = self.regions
            except:
                pass
        if not self._regions:
            raise MapperError('Attribute \'regions\' may not be None (see _regions) .')
        else:
            self._regions = sorted([tpl[0] for tpl in list(self._regions)])

    def get_regions(self):
        if not self._regions:
            self.set_regions()
        return self._regions

    def set_sections(self, choices_tpl=None):
        if choices_tpl:
            if not issubclass(choices_tpl, (tuple, list)):
                raise MapperError('Regions must be a list or choices tuple. Got {0}'.format(choices_tpl))
            self._sections = choices_tpl
        else:
            try:
                self._sections = self.sections
            except:
                pass
        if not self._sections:
            raise MapperError('Attribute \'sections\' may not be None (see _sections) .')

    def get_sections(self):
        if not self._sections:
            self.set_sections()
        return self._sections

    def set_landmarks(self, tpl=None):
        if tpl:
            if not issubclass(tpl, (tuple, list)):
                raise MapperError('landmarks must an instance of tuple or list')
            self._landmarks = tpl
        else:
            try:
                self._landmarks = self.landmarks
            except:
                pass
        if not self._landmarks:
            raise MapperError('Attribute \'_landmarks\' may not be None (see _landmarks) .')

    def get_landmarks(self):
        if not self._landmarks:
            self.set_landmarks()
        return self._landmarks

    def prepare_created_filter(self):
        date_list_filter = []
        today = date.today() + timedelta(days=0)
        tomorrow = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=1)
        last_7days = date.today() - timedelta(days=7)
        last_30days = date.today() - timedelta(days=30)
        #created__lt={0},created__gte={1}
        date_list_filter.append(["Any date", ""])
        date_list_filter.append(["Today", "{0},{1}".format(tomorrow, today)])
        date_list_filter.append(["Yesterday", "{0},{1}".format(today, yesterday)])
        date_list_filter.append(["Past 7 days", "{0},{1}".format(tomorrow, last_7days)])
        date_list_filter.append(["Past 30 days", "{0},{1}".format(tomorrow, last_30days)])
        return date_list_filter

    def make_dictionary(self, list1, list2):
        #the shortest list should be the first list if the lists do
        #not have equal number of elements
        sec_icon_dict = {}
        for sec, icon in zip(list1, list2):
            if sec:
                sec_icon_dict[sec] = icon
            else:
                break
        return sec_icon_dict

    def session_to_string(self, identifiers, new_line=True):
        val = ""
        delim = ", "
        if identifiers:
            # TODO:
            for identifier in identifiers:
                val = val + identifier + delim
        return val

    def prepare_map_points(self, items, selected_icon, cart, cart_icon, dipatched_icon='red-circle', selected_section="All"):
        """Returns a list of item identifiers from the given queryset excluding those items that have been dispatched.
        """
        payload = []
        icon_number = 0
        if selected_section == "All":
            section_color_code_dict = self.make_dictionary(self.get_sections(), self.get_other_icons())
        else:
            section_color_code_dict = self.make_dictionary(self.get_sections(), self.get_icons())
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                    "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        for item in items:
            identifier_label = str(getattr(item, self.identifier_field_attr))
            other_identifier_label = ""
            if getattr(item, self.other_identifier_field_attr):  # e.g. cso_number
                other_identifier_label = str("  {0}: ".format(self.other_identifier_field_label) + getattr(self.other_identifier_field_attr))
            if item.is_dispatched_as_item():
                icon = dipatched_icon
                identifier_label = "{0} already dispatched".format(identifier_label)
            elif getattr(item, self.identifier_field_attr) in cart:  # e.g household_identifier
                icon = cart_icon
                identifier_label = "{0} in shopping cart waiting to be dispatched".format(identifier_label)
            else:
                icon = "blu-circle"
                if selected_section == "All":
                    icon = "blu-circle"
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if item.ward_section == key_sec:
                            if icon_number <= 100:
                                icon = icon_value + str(icon_number)
                                icon_number += 1
                        if icon_number == 100:
                            icon_number = 0
                else:
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if item.ward_section == key_sec:
                            if icon_number <= 25:
                                icon = icon_value + letters[icon_number]
                                icon_number += 1
                            if icon_number == 25:
                                icon_number = 0
            payload.append([item.lon, item.lat, identifier_label, icon, other_identifier_label])
        return payload
