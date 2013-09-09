from vtown import geo                   # pip install geo-utils or download at https://pypi.python.org/pypi/geo-utils
from vtown.geo.polygon import Polygon   # pip install geo-utils or download at https://pypi.python.org/pypi/geo-utils
import math

from geopy import distance
from geopy import Point
from datetime import date, timedelta
from django.conf import settings
from django.utils.encoding import smart_str
from bhp_base_model.models import BaseUuidModel
from bhp_map.exceptions import MapperError


class Mapper(object):

    def __init__(self, *args, **kwargs):
        self._map_area = None
        self._radius = None
        self._item_model_cls = None
        self._item_label = None
        self._regions = None
        self._sections = None
        self._icons = None
        self._other_icons = None
        self._landmarks = None
        self._region_label = None
        self._section_label = None
        self._region_field_attr = None
        self._section_field_attr = None
        self._identifier_field_attr = None
        self._identifier_label = None
        self._other_identifier_field_attr = None  # e.g. cso_number
        self._other_identifier_label = None
        self._gps_center_lat = None
        self._gps_center_lon = None
        self._target_gps_lon_field_attr = None
        self._target_gps_lat_field_attr = None
        self._map_area_field_attr = None

        # item_model_cls
        if 'map_area' in kwargs:
            self.set_map_area(kwargs.get('map_area'))
        #if 'radius' in kwargs:
        #    self.set_radius(kwargs.get('radius'))
        if 'item_model' in kwargs:
            self.set_item_model_cls(kwargs.get('item_model'))
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
        if 'item_label' in kwargs:
            self.set_item_label(kwargs('item_label'))

    def __repr__(self):
        try:
            u = unicode(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<%s: %s>' % (self.__class__.__name__, u))

    def _get_attr(self, attrname):
        if not attrname:  # attrname is the class variable name
            raise TypeError('attrname may not be None.')
        _name = '_{0}'.format(attrname)  # the instance variable name
        if not getattr(self, _name):  # if instance variable is not set
            getattr(self, 'set_{0}'.format(attrname))()
        return getattr(self, _name)

    def _set_attr(self, attrname, attr=None, allow_none=False):
        if attrname.startswith('_'):
            raise TypeError('attrname cannot start with \'_\'')
        if attr:
            setattr(self, '_{0}'.format(attrname), attr)  # set the instance variable to attr
        else:
            try:
                setattr(self, '_{0}'.format(attrname), getattr(self, attrname))  # set the instance variable to the value of the class variable.
            except:
                pass
        if not allow_none:
            if not getattr(self, '_{0}'.format(attrname)):
                raise MapperError('Attribute \'{0}\' may not be None.'.format(attrname))

    def set_map_area(self, attr=None):
        self._set_attr('map_area', attr)

    def get_map_area(self):
        return self._get_attr('map_area')

    def set_radius(self, attr=None):
        self._set_attr('radius', attr)

    def get_radius(self):
        return self._get_attr('radius')

    def set_gps_center_lat(self, attr=None):
        self._set_attr('gps_center_lat', attr)

    def get_gps_center_lat(self):
        return self._get_attr('gps_center_lat')

    def set_gps_center_lon(self, attr=None):
        self._set_attr('gps_center_lon', attr)

    def get_gps_center_lon(self):
        return self._get_attr('gps_center_lon')

    def set_identifier_field_attr(self, attr=None):
        self._set_attr('identifier_field_attr', attr)

    def get_identifier_field_attr(self):
        return self._get_attr('identifier_field_attr')
    
    def set_target_gps_lon_field_attr(self, attr=None):
        self._set_attr('target_gps_lon_field_attr', attr)

    def get_target_gps_lon_field_attr(self):
        return self._get_attr('target_gps_lon_field_attr')
    
    def set_target_gps_lat_field_attr(self, attr=None):
        self._set_attr('target_gps_lat_field_attr', attr)

    def get_target_gps_lat_field_attr(self):
        return self._get_attr('target_gps_lat_field_attr')

    def set_other_identifier_field_attr(self, attr=None):
        self._set_attr('other_identifier_field_attr', attr)

    def get_other_identifier_field_attr(self):
        return self._get_attr('other_identifier_field_attr')

    def set_identifier_label(self, attr=None):
        self._set_attr('identifier_label', attr)

    def get_identifier_label(self):
        return self._get_attr('identifier_label')

    def set_other_identifier_label(self, attr=None):
        self._set_attr('other_identifier_label', attr)

    def get_other_identifier_label(self):
        return self._get_attr('other_identifier_label')

    def set_region_field_attr(self, attr=None):
        self._set_attr('region_field_attr', attr)

    def get_region_field_attr(self):
        return self._get_attr('region_field_attr')

    def set_region_label(self, attr=None):
        self._set_attr('region_label', attr, allow_none=True)
        if not self._region_label:
            self._region_label = self.get_region_field_attr()

    def get_region_label(self):
        return self._get_attr('region_label')

    def set_section_field_attr(self, attr=None):
        self._set_attr('section_field_attr', attr)

    def get_section_field_attr(self):
        return self._get_attr('section_field_attr')

    def set_section_label(self, attr=None):
        self._set_attr('section_label', attr, allow_none=True)
        if not self._section_label:
            self._section_label = self.get_section_field_attr()

    def get_section_label(self):
        return self._get_attr('section_label')
    
    def set_map_area_field_attr(self, attr=None):
        self._set_attr('map_area_field_attr', attr, allow_none=True)
        if not self._map_area_field_attr:
            self._map_area_field_attr = self.get_map_area_field_attr()

    def get_map_area_field_attr(self):
        return self._get_attr('map_area_field_attr')

    def set_item_label(self, attr=None):
        self._set_attr('item_label', attr, allow_none=True)
        if not self._item_label:
            self._item_label = self.get_item_model_cls()._meta.object_name

    def get_item_label(self):
        return self._get_attr('item_label')

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
                if not self.item_model_cls:
                    raise MapperError('Attribute \'item_model_cls\' may not be None (see _item_model_cls) .')
                self._item_model_cls = self.item_model_cls
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

    def _get_as_choices(self, lst):
        if not lst:
            raise AttributeError('Attribute lst cannot be None')
        if not isinstance(lst, list):
            raise TypeError('Attribute lst should be of type \'list\'. Got {0}'.format(lst))
        lst = []
        for c in self.get_regions():
            lst.append((c, c))
        choices = tuple(lst)
        return choices

    def get_regions_as_choices(self):
        return self._get_as_choices(self.get_regions())

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
        else:
            self._sections = sorted([choices_tpl[0] for choices_tpl in list(self._sections)])

    def get_sections(self):
        if not self._sections:
            self.set_sections()
        return self._sections

    def get_sections_as_choices(self):
        return self.get_sections()

    def get_sections_as_tuple(self):
        return self.get_sections()

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
            identifier_label = str(getattr(item, self.get_identifier_field_attr()))
            other_identifier_label = ""
            if getattr(item, self.get_other_identifier_field_attr()):  # e.g. cso_number
                other_identifier_field_label = str("  {0}: ".format(self.other_identifier_field_label) + getattr(item, self.get_other_identifier_field_attr()))
            if item.is_dispatched_as_item():
                icon = dipatched_icon
                identifier_label = "{0} already dispatched".format(identifier_label)
            elif getattr(item, self.get_identifier_field_attr()) in cart:  # e.g household_identifier
                icon = cart_icon
                identifier_label = "{0} in shopping cart waiting to be dispatched".format(identifier_label)
            else:
                icon = "blu-circle"
                if selected_section == "All":
                    icon = "blu-circle"
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if item.section == key_sec:
                            if icon_number <= 100:
                                icon = icon_value + str(icon_number)
                                icon_number += 1
                        if icon_number == 100:
                            icon_number = 0
                else:
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if item.section == key_sec:
                            if icon_number <= 25:
                                icon = icon_value + letters[icon_number]
                                icon_number += 1
                            if icon_number == 25:
                                icon_number = 0
            payload.append([item.gps_target_lon, item.gps_target_lat, identifier_label, icon, other_identifier_label])
        return payload

    def gps_distance_between_points(self, lat, lon, center_lat=None, center_lon=None, radius=None):
        """Check if a GPS point is within the boundaries of a community

        This method uses geopy.distance and geopy.Point libraries to calculate the distance betweeen two points
        and return the distance in units requested. The community radius is used to check is a point is within a
        radius of the community.

        The community_radius, community_center_lat and community_center_lon are from the Mapper class of each community.
        """
        center_lat = center_lat or self.get_gps_center_lat()
        center_lon = center_lon or self.get_gps_center_lon()
        radius = radius or self.get_radius()
        pt1 = Point(float(lat), float(lon))
        pt2 = Point(float(center_lat), float(center_lon))
        dist = distance.distance(pt1, pt2).km
        return dist

    def deg_to_dms(self, deg):
        """Convert a latitude or longitude into degree minute GPS format
        """
        d = int(deg)
        md = (deg - d) * 60
        m = round(md, 3)
        if d < 0 and m < 0:
            d = -d
            m = -m
        return [d, m]

    def get_cardinal_point_direction(self, start_lat, start_lon, end_lat, end_lon):
        """Calculates the angle/Bearing of direction between two points on the earth and returns the distance between two points and the cardinal points direction.

        This method is for the initial bearing which if followed in a straight line
        along a great-circle arc will take you from the start point to the end point.
        """
        dist = self.distance_between_points(start_lat, start_lon, end_lat, end_lon)
        dlon = math.radians(end_lon - start_lon)
        start_lat = math.radians(start_lat)
        end_lat = math.radians(end_lat)
        y = math.sin(dlon) * math.cos(end_lat)
        x = math.cos(start_lat) * math.sin(end_lat) - math.sin(start_lat) * math.cos(end_lat) * math.cos(dlon)
        brng = math.degrees(math.atan2(y, x))
        bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        index = brng - 22.5
        if (index < 0):
            index += 360
        index = int(index / 45)

        return(round(dist, 3), bearings[index])

    def _get_gps(self, direction, degrees, minutes):
        """Converts GPS degree/minutes to latitude or longitude."""
        dct = {'s': -1, 'e': 1}
        if direction not in dct.keys():
            raise TypeError('Direction must be one of {0}. Got {1}.'.format(dct.keys(), direction))
        d = float(degrees)
        m = float(minutes)
        return dct[direction] * round((d) + (m / 60), 5)

    def get_gps_lat(self, d, m):
        """Converts degree/minutes S to latitude."""
        return self._get_gps('s', d, m)

    def get_gps_lon(self, d, m):
        """Converts degree/minutes E to longitude."""
        return self._get_gps('e', d, m)

    def verify_gps_location(self, lat, lon, exception_cls):
        """Verifies that given lat, lon occur within the community area and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        if not self.gps_distance_between_points(lat, lon):
            raise exception_cls('The location (GPS {0} {1}) does not fall within this community.'.format(lat, lon))
        return True

    def verify_gps_to_target(self, lat, lon, center_lat, center_lon, radius, exception_cls):
        """Verifies the gps lat, lon occur within a radius of the target lat/lon and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        verify = True
        if 'VERIFY_GPS' in dir(settings):
            verify = settings.VERIFY_GPS
        if verify:
            dist = self.gps_distance_between_points(lat, lon, center_lat, center_lon, radius)
            if dist > radius:
                raise exception_cls('GPS {0} {1} is more than {2} meters from the target location.'.format(lat, lon, radius * 1000))
        return True
