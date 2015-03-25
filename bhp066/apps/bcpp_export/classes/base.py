from collections import OrderedDict, namedtuple
from copy import copy
from datetime import datetime
from uuid import uuid4

from django.core.exceptions import MultipleObjectsReturned

from edc.base.model.fields.helpers import site_revision
from edc.constants import YES, NO
from edc.map.classes import site_mappers

DescriptionTuple = namedtuple('DescriptionTuple', 'value type tag')


class NewOrderedDict(OrderedDict):
    @property
    def unique_key(self):
        return self['unique_key']


class Base(object):

    def __init__(self, verbose=None):
        self.verbose = verbose
        site_mappers.autodiscover()
        self.customized = False
        self._data = NewOrderedDict()
        self.export_uuid = unicode(uuid4())
        self.timestamp = datetime.today().isoformat()

    @property
    def data(self):
        """Returns an ordered dictionary of the instance attributes.

        To see this as a dictionary:
            >>> dict(instance.data)"""

        if not self._data:
            keys = self.__dict__.keys()
            keys.append('export_revision')
            keys.append('revision')
            keys.sort()
            keys.insert(0, 'unique_key')
            for key in keys:
                try:
                    self._data[key] = copy(self.__dict__[key])
                except KeyError:
                    self._data[key] = None
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
            self._data['export_revision'] = self.export_revision
            self._data['unique_key'] = self.unique_key
        return self._data

    @property
    def export_revision(self):
        return str(site_revision)

    def customize_for_csv(self, isoformat=None):
        """Modifies values in the 'data' attribute to be more friendly for CSV export."""
        if self.customized:
            raise TypeError('Method cannot be called twice')
        self.customized = True
        for key, value in self.data.iteritems():
                # convert booleans to YES/NO
            if value is None:
                self.data[key] = ''
            elif value is True or value == 'True':
                self.data[key] = YES
            elif value is False or value == 'False':
                self.data[key] = NO
            else:
                try:
                    self.data[key] = value.isoformat() if isoformat else value.strftime('%Y-%m-%d')
                except AttributeError:
                    pass
                except ValueError:
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
        lookup_flds = {}
        for fldname, attrname in fieldattrs:
            # set attribute on self to None
            attrname = '{}_{}'.format(attrname, attr_suffix.lower())
            setattr(self, attrname, None)
            try:
                # try to set value from instance
                field_value = getattr(instance, fldname)
                setattr(self, attrname, field_value)
            except AttributeError:
                if lookup_model:
                    # collect fields/attrs for query below
                    lookup_flds.update({fldname: attrname})
        if lookup_flds:
            try:
                values = lookup_model.objects.values(
                    *lookup_flds).get(
                    **{lookup_string: lookup_instance})
                for fld, value in values.iteritems():
                    setattr(self, lookup_flds[fld], value)
            except lookup_model.DoesNotExist:
                for attr in lookup_flds.values():
                    setattr(self, attr, None)
            except MultipleObjectsReturned:
                values_queryset = lookup_model.objects.values(
                    *lookup_flds).filter(
                    **{lookup_string: lookup_instance})
                for values in values_queryset:
                    vals = []
                    for fld, value in values.iteritems():
                        vals.append(value)
                    setattr(self, lookup_flds[fld], ';'.join(vals))
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
