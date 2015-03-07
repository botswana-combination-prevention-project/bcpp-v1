from collections import OrderedDict
from datetime import datetime
from uuid import uuid4

from django.core.exceptions import MultipleObjectsReturned


class BaseHelper(object):

    def __init__(self):
        self.customized = False
        self._data = OrderedDict()
        self.export_uuid = unicode(uuid4())
        self.timestamp = datetime.today().strftime('%Y%m%d%H%M%S%s')

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

    def customize_for_csv(self):
        """Modifies values in the 'data' attribute to be more friendly for CSV export."""
        if self.customized:
            raise TypeError('Method cannot be called twice')
        self.customized = True
        for key, value in self.data.iteritems():
            try:
                self.data[key] = value.strftime('%Y-%m-%d')
            except AttributeError:
                pass
            if isinstance(value, (list, tuple)):
                try:
                    self.data[key] = ','.join([v.strftime('%Y-%m-%d') for v in value])
                except (TypeError, AttributeError):
                    try:
                        self.data[key] = ','.join(value)
                    except (TypeError, AttributeError):
                        pass
            if value is None:
                self.data[key] = ''

    def _update(self, survey_abbrev, fieldattrs, model_cls, lookup_string, household_member):
        """Dynamically sets one or more instance attributes and adds the survey_abbrev suffix.

        This unormalizes or flattens the values relative to a survey. If this method is called
        in a loop on Survey for surveys [Y1, Y2, Y3] an attribute name 'example_attribute' would
        be set as example_attribute_y1, example_attribute_y2, example_attribute_y3.

        For example::
            fieldattrs = [('report_datetime', 'member_absent_date'),
                          ('absent', 'member_absent')]
            model_cls = SubjectAbsenteeEntry
            for survey in Survey.objects.all():
                subject_absentee_entry = self._update(
                    survey.survey_abbrev, fieldattrs, model_cls,
                    'subject_absentee__household_member',
                    self.household_membership_survey.get(survey.survey_slug)
                    )

        >>> dir(self)
        [ ...,
        member_absent_y1, member_absent_y3, member_absent_y3,
        ...,
        member_absent_date_y1, member_absent_date_y2, member_absent_date_y3,
        ...]
        """
        instance = None
        for fldname, attrname in fieldattrs:
            if not lookup_string:
                instance = household_member
                if instance:
                    setattr(self, '{}_{}'.format(attrname, survey_abbrev.lower()), getattr(instance, fldname))
                else:
                    setattr(self, '{}_{}'.format(attrname, survey_abbrev.lower()), None)
            else:
                try:
                    instance = model_cls.objects.get(
                        **{lookup_string: household_member})
                    setattr(self, '{}_{}'.format(attrname, survey_abbrev.lower()), getattr(instance, fldname))
                except model_cls.DoesNotExist:
                    setattr(self, '{}_{}'.format(attrname, survey_abbrev.lower()), None)
                except MultipleObjectsReturned:
                    values = []
                    instances = model_cls.objects.filter(**{lookup_string: household_member})
                    for instance in instances:
                        values.append(getattr(instance, fldname))
                    setattr(self, '{}_{}'.format(attrname, survey_abbrev.lower()), values)
        return instance
