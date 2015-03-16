from collections import OrderedDict, namedtuple
from datetime import datetime
from uuid import uuid4

from django.core.exceptions import MultipleObjectsReturned

from edc.base.model.fields.helpers import site_revision
from edc.map.classes import site_mappers

DescriptionTuple = namedtuple('DescriptionTuple', 'value type tag')


class Base(object):

    def __init__(self, verbose=None):
        self.verbose = verbose
        site_mappers.autodiscover()
        self.customized = False
        self._data = OrderedDict()
        self.export_uuid = unicode(uuid4())
        self.timestamp = datetime.today().isoformat()

    @property
    def data(self):
        """Returns an ordered dictionary of the instance attributes.

        To see this as a dictionary:
            >>> dict(instance.data)"""

        if not self._data:
            keys = self.__dict__.keys()
            keys.sort()
            for key in keys:
                self._data[key] = self.__dict__[key]
            try:
                del self._data['_data']
            except KeyError:
                pass
            try:
                del self._data['_data_errors']
            except KeyError:
                pass
            try:
                del self._data['errors']
            except KeyError:
                pass
        return self._data

    @property
    def revision(self):
        return str(site_revision)

    def customize_for_csv(self, isoformat=None):
        """Modifies values in the 'data' attribute to be more friendly for CSV export."""
        if self.customized:
            raise TypeError('Method cannot be called twice')
        self.customized = True
        for key, value in self.data.iteritems():
            if value is None:
                self.data[key] = ''
            else:
                try:
                    self.data[key] = value.isoformat() if isoformat else value.strftime('%Y-%m-%d')
                except AttributeError:
                    pass
                if isinstance(value, (list, tuple)):
                    for index, v in enumerate(value):
                        if v is None:
                            self.data[key][index] = ''
                        else:
                            try:
                                self.data[key][index] = v.isoformat() if isoformat else v.strftime('%Y-%m-%d')
                            except AttributeError:
                                pass
                    try:
                        self.data[key] = ','.join(value)
                    except TypeError:
                        pass
        del self.data['customized']
        del self.data['verbose']

    def denormalize(self, attr_suffix, fieldattrs, instance=None,
                    lookup_model=None, lookup_instance=None, lookup_string=None):
        """Denormalizes one or more instance attributes and adds the survey_abbrev suffix.

        This denormalize or flattens the values relative to a survey. If this method is called
        in a loop on Survey for surveys [Y1, Y2, Y3] an attribute name 'example_attribute' would
        be set as example_attribute_y1, example_attribute_y2, example_attribute_y3.

        For example::
            attr_suffix = suffix to add to an attr name that the data is denormalized on
            fieldattrs = [('report_datetime', 'member_absent_date'),
                          ('absent', 'member_absent')]
            for survey in Survey.objects.all():
                attr_suffix = survey.survey_abbrev
                subject_absentee_entry = self.denormalize((
                    attr_suffix, fieldattrs,
                    lookup_model=SubjectAbsenteeEntry
                    lookup_string='subject_absentee__household_member',
                    lookup_instance=self.household_membership_survey.get(survey.survey_slug)
                    )

        >>> dir(self)
        [ ...,
        member_absent_y1, member_absent_y3, member_absent_y3,
        ...,
        member_absent_date_y1, member_absent_date_y2, member_absent_date_y3,
        ...]
        """
        obj = None
        for fldname, attrname in fieldattrs:
            attrname = '{}_{}'.format(attrname, attr_suffix.lower())
            try:
                field_value = getattr(instance, fldname)
                setattr(self, attrname, field_value)
            except AttributeError:
                if not lookup_model:
                    setattr(self, attrname, None)
                else:
                    try:
                        obj = lookup_model.objects.get(
                            **{lookup_string: lookup_instance})
                        setattr(self, attrname, getattr(obj, fldname))
                    except lookup_model.DoesNotExist:
                        setattr(self, attrname, None)
                    except MultipleObjectsReturned:
                        field_values = []
                        insts = lookup_model.objects.filter(**{lookup_string: lookup_instance})
                        for inst in insts:
                            field_values.append(getattr(inst, fldname))
                        setattr(self, attrname, field_values)
        return obj

    def denormalize_other(self, attr_suffix, fieldattrs, instance):
        """Adds denormalized attrs to self from "Other Specify ..." fields

        If the value of attr 'fldname' is 'OTHER' uses the value of 'other_fldname'."""
        for fldname, other_fldname, attrname in fieldattrs:
            attrname = '{}_{}'.format(attrname, attr_suffix.lower())
            try:
                if getattr(instance, fldname) == 'OTHER':
                    field_value = getattr(instance, other_fldname)
                else:
                    field_value = getattr(instance, fldname)
                setattr(self, attrname, field_value)
            except AttributeError:
                setattr(self, attrname, None)

    def normalize(self, instance, attrname, attr_suffix_list):
        values = []
        for attr_suffix in attr_suffix_list:
            print getattr(instance, '{}_{}'.format(attrname, attr_suffix))
            values.append(getattr(instance, '{}_{}'.format(attrname, attr_suffix)))
        return values
