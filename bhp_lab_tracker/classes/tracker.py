import logging
from datetime import datetime
from django.db.models import ForeignKey, OneToOneField, get_model
from django.core.exceptions import ImproperlyConfigured
from bhp_base_model.models import BaseModel
from bhp_lab_tracker.models import HistoryModel, DefaultValueLog
from helpers import TrackerNamedTpl
from history_updater import HistoryUpdater


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class LabTracker(object):
    """An abstract class to track or maintain a history of subject's lab result value from both the lab_clinic_api models ands protocol scheduled model(s).

    Required class attributes to be defined on the subclass:
        * resultitem_test_code: a tuple of test codes for reference to the :mod:`lab_clinic_api.result_item`.
          For example: ('ELISA', 'RELISA', 'DNAPCR')
        * tracker_test_code = a test code to use for results coming from a registered model.
          For example: 'HIV'
        * group_name = a label to group all records in the history model related to this class instance.
          Must be unique for each type of value being tracked. For example: 'HIV'.

    Optional class attributes to be defined on the subclass:
        * trackers: a list of tuples where the containing tuple defines (model_cls, value_attr, date_attr).
          Use this attribute to include models from your app that capture values not captured in
          model :class:`lab_clinic_api.models.ResultItem`.

        .. note:: If \'trackers\' is not defined, the class will just track values in :mod:`lab_clinic_api.result_item`.

    For example::

        class InfantHivLabTracker(HivLabTracker):
            trackers = [
                (HivTesting, 'pcr_result', 'pcr_date', None, True),
                (HivTesting, 'elisa_result', 'elisa_date', None, True)]
        lab_tracker.register(InfantHivLabTracker)

    You may also need to add a method on the model to return a known value. For example, for HIV::

        def get_result_value(self, attr=None):
            retval = None
            if not attr in dir(self):
                raise TypeError('Attribute {0} does not exist in model {1}'.format(attr, self._meta.object_name))
            if attr == 'is_hiv_pos':
                if self.is_hiv_pos.lower() == 'yes':
                    retval = 'POS'
                else:
                    retval = 'NEG'
            return retval
    """

    MODEL_CLS = 0
    VALUE_ATTR = 1
    DATE_ATTR = 2
    IDENTIFIER_ATTR = 3
    ALLOW_NULL = 4
    models = None
    trackers = None
    group_name = None
    tracked_test_codes = None
    subject_type = None

    def __init__(self, subject_identifier=None):
        """If the user does not declare self.models, the tracker will add result_item so that the
        tracker at least gets what's in lab_clinic_api tables."""
        self._result_item_tracker = None
        self._trackers = None
        self._models = None
        self._group_name = None
        self._subject_identifier = None
        self._value_datetime = None
        self._is_default_value = None
        self._value = None
        self._history = None
        self._tracked_test_codes = None
        self._test_code = None
        self._history_inst = None
        self._subject_type = None
        self._history_query_options = None
        self._is_dirty = True
        self._subject_type = None
        self._init_subject_identifier = subject_identifier

    def set_result_item_tracker(self):
        """Sets the tracker for lab_clinic_api.result_item which is added by default to the list of trackers."""
        self._result_item_tracker = TrackerNamedTpl(
            model_cls=get_model('lab_clinic_api', 'resultitem'),
            value_attr='result_item_value',
            datetime_attr='result_item_datetime',
            identifier_attr='result__order__order_identifier',
            allow_null=False)

    def get_result_item_tracker(self):
        if not self._result_item_tracker:
            self.set_result_item_tracker()
        return self._result_item_tracker

    def _set_is_dirty(self, value):
        self._is_dirty = value

    def is_dirty(self):
        return self._is_dirty

    def set_value(self):
        """Sets the result value relative to value_datetime OR the default value if there is no
        information for this subject in the History model."""
        self._value = self._get_history_inst().value
        if not self._value:
            self._value = self._get_default_value()
            self._log_default_value_used()
        if not self._value:
            raise TypeError('Unable to determine the current value. May not be None.')
        self._set_is_dirty(False)

    def get_value(self, value_datetime=None):
        if value_datetime:
            self.set_value_datetime(value_datetime)
        if not self._value or self.is_dirty():
            self.set_value()
        return self._value

    def set_history(self, order_desc=None):
        """Sets to an ordered HistoryModel queryset for this subject filtered for records on or before value_datetime."""
        self._history = None
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        self.update_history()
        options = {'subject_identifier': self.get_subject_identifier(),
                   'group_name': self.get_group_name()}
        options.update({'value_datetime__lte': self.get_value_datetime()})
        self._history = HistoryModel.objects.filter(**options).order_by(order_by)

    def get_history(self, value_datetime, order_desc=None):
        """Returns an ordered HistoryModel queryset for this subject filtered for records on or before value_datetime."""
        if order_desc == None:
            order_desc = True
        self.set_value_datetime(value_datetime)
        if not self._history or self.is_dirty():
            self.set_history(order_desc)
        return self._history

    def get_history_as_list(self, reference_datetime=None):
        """Returns all values on or before :attr:`reference_datetime` for a subject as a list in ascending chronological order."""
        if not reference_datetime:
            reference_datetime = self.get_value_datetime()
        queryset = self.get_history(reference_datetime, order_desc=False)
        return [qs.value for qs in queryset]

    def get_history_as_string(self, reference_datetime, mapped=None):
        """Returns a subject's qualitative values joined as a string in ascending chronological order.

        Args:
            * mapped: if False do not attempt to use a display map (default=True).

        If :attr:`mapped` is True and a display map is defined in :func:`get_display_map_prep`, the display map is
        inverted and a string of values is generated from the map."""
        if self._get_display_map():
            mapped = True
        retlst = []
        inv_display_map = {}
        if mapped:
            for k, v in self._get_display_map().iteritems():
                inv_display_map.update({v: inv_display_map.get(v, [k])})
        history = self.get_history_as_list(reference_datetime)
        for item in history:
            if mapped:
                if item in inv_display_map:
                    retlst.append(inv_display_map[item][0].lower())
                else:
                    retlst.append(item)  # value not in map, so just append the value, almost an error...
            else:
                retlst.append(item)
        return ''.join(retlst)

    def set_is_default_value(self, is_default_value=None):
        self._is_default_value = is_default_value or False

    def get_is_default_value(self):
        if not self._is_default_value:
            self.set_is_default_value()
        return self._is_default_value

    def set_subject_type(self, value=None):
        self._subject_type = value or self.subject_type
        if not self._subject_type:
            raise ImproperlyConfigured('Attribute _subject_type may not be None. Specify at the class declaration (e.g. subject_type = \'infant\'. See tracker {0}'.format(self))
        if not isinstance(self.subject_type, basestring):
            raise ImproperlyConfigured('Attribute _subject_type must be a string. Got {0}. Specify at the class declaration (e.g. subject_type = \'infant\''.format(self._subject_type))

    def get_subject_type(self):
        if not self._subject_type:
            self.set_subject_type()
        return self._subject_type

    def set_trackers(self):
        self._trackers = []
        if not self.trackers:
            self.trackers = []
        # add the default "result item" tuple, need this one at least
        if self.get_result_item_tracker() not in self.trackers:
            self.trackers.append(self.get_result_item_tracker())
        for tracker in self.trackers:
            if not isinstance(tracker, TrackerNamedTpl):
                # trackers are declared as tuples but must be named tuples, so convert
                tracker = list(tracker)
                tracker.extend([None for x in xrange(len(tracker), len(TrackerNamedTpl._fields))])
                tracker = TrackerNamedTpl(*tracker)
            if not issubclass(tracker.model_cls, BaseModel):
                raise ImproperlyConfigured('tracker tuple element \'model_cls\' must be a Model class. Got {0}'.format(tracker.model_cls))
            if not isinstance(tracker.value_attr, basestring):
                raise ImproperlyConfigured('tracker tuple element \'value_attr\' must be a string. Got {0}'.format(tracker.value_attr))
            if not isinstance(tracker.datetime_attr, basestring):
                raise ImproperlyConfigured('tracker tuple element \'datetime_attr\' must be a string. Got {0}'.format(tracker.datetime_attr))
            if tracker.identifier_attr:
                if not isinstance(tracker.identifier_attr, basestring):
                    raise ImproperlyConfigured('tracker tuple element \'identifier_attr\' must be a string. Got {0}'.format(tracker.identifier_attr))
            self._trackers.append(tracker)

    def get_trackers(self):
        if not self._trackers:
            self.set_trackers()
        return self._trackers

    def set_models(self):
        self._models = []
        for tracker in self.get_trackers():
            self._models.append(tracker.model_cls)
        self._models = tuple(self._models)

    def get_models(self):
        if not self._models:
            self.set_models()
        return self._models

    def set_group_name(self):
        self._group_name = self.group_name
        if not self._group_name:
            raise ImproperlyConfigured('Attribute \'_group_name\' cannot be None. Set \'group_name\' as a class attribute in the class declaration')

    def get_group_name(self):
        if not self._group_name:
            self.set_group_name()
        return self._group_name

    def get_default_value(self):
        """Returns the a value if None is available.

        Users may override, carefully"""
        return 'UNK'

    def _get_default_value(self):
        """Returns the default value when none is available from the HistoryModel."""
        default_value = self.get_default_value()
        self.set_is_default_value(True)
        return default_value

    def _get_default_value_datetime(self):
        return datetime.today()

    def get_value_map_prep(self, model_name):
        """Users should override to use a custom map for a given tracker model."""
        return {}

    def _get_value_map(self, model_name):
        """Maps an instance result value according to a configured map, if such a map exists."""
        # check model exists
        for tracker in self.get_trackers():
            if tracker.model_cls._meta.object_name.lower():
                return self.get_value_map_prep(model_name)
        return None

    def _set_history_query_options(self):
        from bhp_visit_tracking.models import BaseVisitTracking
        self._history_query_options = {}
        for tracker in self.get_trackers():
            query_string = None
            options = None
            if tracker.model_cls == self.get_result_item_tracker().model_cls:
                options = {'result__subject_identifier': self.get_subject_identifier(),
                           'test_code__code__in': self._get_tracked_test_codes()}
            else:
                field_list = [f.name for f in tracker.model_cls._meta.fields]
                if 'subject_identifier' in field_list:
                    query_string = 'subject_identifier'
                elif 'registered_subject' in field_list:
                    query_string = 'registered_subject__subject_identifier'
                else:
                    for field in tracker.model_cls._meta.fields:
                        if isinstance(field, (ForeignKey, OneToOneField)):
                            if issubclass(field.rel.to, BaseVisitTracking):
                                query_string = '{visit_field}__appointment__registered_subject__subject_identifier'.format(visit_field=field.name)
                                break
                if not query_string:
                    raise TypeError(('Missing subject_identifier attribute or a relation to one. The model class {0} is'
                                    ' not a subclass of BaseVisitTracking and nor does it have a relation to RegisteredSubject.').format(tracker.model_cls._meta.object_name))
                options = {query_string: self.get_subject_identifier()}
            if not options:
                raise TypeError('Unable to determine the query options for tracker \'{0}\'.'.format(tracker))
            self._history_query_options.update({tracker: options})

    def _get_history_query_options(self, tracker):
        if not self._history_query_options:
            self._set_history_query_options()
        return self._history_query_options.get(tracker)

    def update_history(self):
        """Updates the HistoryModel with the subject's values found in any registered models and ResultItem."""
        for tracker in self.get_trackers():
            options = self._get_history_query_options(tracker)
            for model_inst in tracker.model_cls.objects.filter(**options):
                HistoryUpdater(model_inst, self.get_group_name(), self.get_subject_type(), tracker=tracker, tracked_test_codes=self._get_tracked_test_codes()).update()

    def set_value_datetime(self, value=None):
        """Sets value_datetime, None is allowed."""
        self._set_is_dirty(True)
        self._value_datetime = value
        if not self._value_datetime:
            raise TypeError('Attribute _value_datetime may not be None.')

    def get_value_datetime(self):
        if not self._value_datetime:
            self.set_value_datetime()
        return self._value_datetime

    def set_subject_identifier(self):
        """Sets the subject_identifier which may not be None."""
        self._subject_identifier = self._init_subject_identifier
        if not self._subject_identifier:
            raise TypeError('Attribute _subject_identifier may not be None.')

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def _set_history_inst(self):
        """Sets to the most recent history model instance relative to the value_datetime or to a default HistoryModel instance.

        The default value is ignore and never reported unless a value does not exist. Make sure the default value is NOT a value
        that might be reported. For example for HIV expect (POS, NEG, IND) so the default value cannot be POS or NEG or IND. Best to keep the
        default value as (UNK) for unknown.

        .. note:: the default value is excluded if a value exists. Some models may have option to report a value in more than one way.
                  For example, a model might ask for the most recent pcr, elisa or last known value. If you report one of these three, such
                  as the last know value (NEG), the other two will supply an UNK for that datetime. So the history for  that datetime is
                  NEG, UNK, UNK. The unknowns (UNK, UNK) should be ignored to report NEG."""
        # create a default instance
        self._history_inst = HistoryModel(
            subject_identifier=self.get_subject_identifier(),
            subject_type=self.get_subject_type(),
            value_datetime=self._get_default_value_datetime(),
            value=self._get_default_value())
        if HistoryModel.objects.filter(subject_identifier=self.get_subject_identifier(),
                                       subject_type=self.get_subject_type(),
                                       group_name=self.get_group_name(),
                                       value_datetime__lte=self.get_value_datetime()).exclude(value=self._get_default_value()).exists():
            # set to most recent relative to value_datetime
            # TODO: this may cause problems for value_datetime when queried by date (with no time)
            self._history_inst = HistoryModel.objects.filter(
                subject_identifier=self.get_subject_identifier(),
                subject_type=self.get_subject_type(),
                group_name=self.get_group_name(),
                value_datetime__lte=self.get_value_datetime()
                ).exclude(value=self._get_default_value()).order_by('-value_datetime')[0]
        self._set_is_dirty(False)

    def _get_history_inst(self):
        if not self._history_inst or self.is_dirty():
            self._set_history_inst()
        return self._history_inst

    def _log_default_value_used(self):
        """Logs that a default value was used. """
        default_value_log = DefaultValueLog.objects.create(
            subject_identifier=self.get_subject_identifier(),
            group_name=self.get_group_name(),
            value=self._get_default_value(),
            value_datetime=self._get_default_value_datetime())
        return default_value_log

    def _get_display_value(self, tracker):
        display_value = self.get_value()
        if display_value:
            display_map = tracker._get_display_map()
            if display_map:
                display_value = display_map.get(self.get_value(), None)
            if not display_value and not tracker.allow_null:
                raise ValueError('Result value \'{0}\' did not match any value in the display map \'{1}\'.'.format(self.get_value(), display_map))
        return display_value

    def _get_display_map(self):
        return self.get_display_map_prep()

    def get_display_map_prep(self):
        """Returns a dictionary that may be used to map values for storage in the :class:`HistoryModel` to value formats used in :class:`ResultItem` model.

            Format {given this value: store this value}.

            This is useful if update_prep adds results that are not described in the same format as the :class:`ResultItem` model.

            For example:
                {'A': 'POS', 'B': NEG} will store POS and NEG given A, B. POS, NEG is how it is stored in the :class:`ResultItem` model.

            Also, the map is inverted to generate a string of values using this map returning 'AB' instead of 'POSNEG'.

            Users may override."""
        return None

    def _set_tracked_test_codes(self):
        self._tracked_test_codes = self.tracked_test_codes
        if not self._tracked_test_codes:
            raise ImproperlyConfigured('Class attribute \'tracked_test_codes\' may not be None. Should be a test code or tuple of test codes. Set \'tracked_test_codes\' in the class declaration for {0}'.format(self))
        if not isinstance(self._tracked_test_codes, (list, tuple)):
            self._tracked_test_codes = (self._tracked_test_codes, )

    def _get_tracked_test_codes(self):
        """Returns a tuple of test codes to track.

        If not listed here, the history model will not be updated with the instance."""
        if not self._tracked_test_codes:
            self._set_tracked_test_codes()
        return self._tracked_test_codes
