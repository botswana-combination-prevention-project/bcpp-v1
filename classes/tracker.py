from datetime import datetime
from django.db.models import ForeignKey, OneToOneField
from django.core.exceptions import ImproperlyConfigured
from lab_clinic_api.models import ResultItem
from bhp_registration.models import RegisteredSubject
from bhp_lab_tracker.models import HistoryModel


class LabTracker(object):
    """An abstract class to track or maintain a history of subject's lab result value from both the lab_clinic_api models ands protocol scheduled model(s).

    Required class attributes to be defined on the subclass:
        * resultitem_test_code: a tuple of test codes for reference to the :mod:`lab_clinic_api.result_item`.
          For example: ('ELISA', 'RELISA', 'DNAPCR')
        * tracker_test_code = a test code to use for results coming from a registered model.
          For example: 'HIV'
        * group_name = a label to group all records in the history model related to this class instance.
          For example: 'HIV'

    Optional class attributes to be defined on the subclass:
        * models: a tuple of tuples where the containing tuple defines (model_cls, value_attr, date_attr)

        .. note:: If models is not defined, the class will just track values in :mod:`lab_clinic_api.result_item`.
    """

    MODEL_CLS = 0
    VALUE_ATTR = 1
    DATE_ATTR = 2
    result_item_tpl = (ResultItem, 'result_item_value', 'result_item_datetime')

    def __init__(self):
        """If the user does not declare self.models, the tracker will just get what's in lab_clinic_api tables."""
        if not 'models' in dir(self):
            self.models = []
        if self.models:
            if not isinstance(self.models, list):
                raise ImproperlyConfigured('Class attribute \'models\' must be a list. Got {0}'.format(self.models))
            for tpl in self.models:
                if not isinstance(tpl, tuple):
                    raise ImproperlyConfigured('Class attribute \'models\' list must contain tuples (model_cls, value_attr, date_attr). Got {0}'.format(self.models))
        # self.models.append(self.add_result_item_tpl())

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

    def _get_value_map(self, model_name):
        """Maps an instance result value according to a configured map, if such a map exists."""
        # check model exists
        for model_tpl in self.models:
            model_cls, value_attr, date_attr = model_tpl
            if model_name == model_cls._meta.object_name.lower():
                return self.get_value_map_prep(model_name)
        return None

    def get_value_map_prep(self, model_name):
        """Users should override to use a custom map for a given tracker model."""
        return {}

    def update(self, subject_identifier):
        """Updates the HistoryModel with the subject's values found in any registered models and ResultItem."""
        if self.models:
            self._update_from_tracker_models(subject_identifier)
        self._update_from_result_item(subject_identifier)

    def update_with_tracker_instance(self, instance, model_tpl):
        """Updates the history model given a registered tracker model instance."""
        model_cls, value_attr, date_attr = model_tpl
        self._update_history_model(
            instance._meta.object_name.lower(),
            instance.get_subject_identifier(),
            self._get_tracker_test_code(),
            self._get_tracker_result_value(instance, value_attr),
            self._get_tracker_result_datetime(instance, date_attr),
            )

    def _update_from_tracker_models(self, subject_identifier):
        """Loops through all registered models and updates the history.

        Excludes ResultItem
        """
        from bhp_visit_tracking.models import BaseVisitTracking
        result_item_cls = self.result_item_tpl[self.MODEL_CLS]
        for model_cls, value_attr, date_attr in self.models:
            if model_cls != result_item_cls:
                for field in model_cls._meta.fields:
                    if isinstance(field, (ForeignKey, OneToOneField)):
                        if issubclass(field.rel.to, BaseVisitTracking):
                            query_string = '{visit_field}__appointment__registered_subject__subject_identifier'.format(visit_field=field.name)
                            break
                        if field.rel.to == RegisteredSubject:
                            query_string = 'registered_subject__subject_identifier'
                            break
                if not query_string:
                    raise TypeError(('Cannot determine link to subject_identifier. The model class {0} is'
                                    ' not a subclass of BasVisitTracking and nor does it have a relation to RegisteredSubject.').format(model_cls._meta.object_name))
                options = {query_string: subject_identifier}
                #options = {'registered_subject__subject_identifier': subject_identifier}
                queryset = model_cls.objects.filter(**options)
                #except:
                #    AttributeError('Lab Tracker model {0} must have a key to either a visit model or RegisteredSubject'.format(model._meta.object_name))
                for instance in queryset:
                    self.update_with_tracker_instance(instance, (model_cls, value_attr, date_attr))

    def _update_history_model(self, source, subject_identifier, test_code, value, value_datetime):
        """Inserts or Updates the history model using a using get_or_create() with the given criteria."""
        history_model, created = HistoryModel.objects.get_or_create(
            source=source,
            group_name=self._get_group_name(),
            subject_identifier=subject_identifier,
            test_code=test_code,
            value_datetime=value_datetime,
            defaults={'value': value})
        if not created:
            history_model.value = value
            history_model.modified = datetime.today()
            history_model.save()

    def _update_from_result_item(self, subject_identifier):
        """Updates the history model from values in ResultItem for this subject."""
        result_item_cls = self.result_item_tpl[self.MODEL_CLS]
        value_attr = self.result_item_tpl[self.VALUE_ATTR]
        date_attr = self.result_item_tpl[self.DATE_ATTR]
        for result_item in result_item_cls.objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=self._get_resultitem_test_codes()):
            self._update_history_model('resultitem', subject_identifier, result_item.test_code.code, getattr(result_item, value_attr), getattr(result_item, date_attr))

    def _get_resultitem_test_codes(self):
        """Returns a tuple of test codes that appear in ResultItem and are of interest to this tracker."""
        if not self.resultitem_test_code:
            raise AttributeError('Class attribute \'resultitem_test_code\' cannot be None. Should be a test code or tuple of test codes.')
        if not isinstance(self._test_code, (list, tuple)):
            self.resultitem_test_code = (self.resultitem_test_code, )
        return self.resultitem_test_code

    def _get_tracker_test_code(self):
        """Returns a user defined test code to use on results put together from a registered model."""
        if not self.tracker_test_code:
            raise AttributeError('Class attribute \'tracker_test_code\' cannot be None. Should be the test code used for tracker model results')
        return self.tracker_test_code

    def _get_group_name(self):
        """Returns a group_name or 'name' to group values in the history model for this class."""
        return self.group_name

    def _get_tracker_result_datetime(self, instance, date_attr=None):
        """Returns the datetime of the result item value determined either by getting the instance
        attribute or calling the instance method :func:`get_result_datetime` with the attribute name.

        Args:
            * date_attr: instance attribute name on instance that has the datetime (default: result_item_datetime)
        """
        if not date_attr:
            # default to attr name in result_item model
            date_attr = 'result_item_datetime'
        if 'get_result_datetime' in dir(instance):
            retval = instance.get_result_datetime(date_attr)
        else:
            retval = getattr(instance, date_attr)
        return retval

    def _get_tracker_result_value(self, instance, value_attr=None):
        """Returns a result item value which, if a map exists, is mapped to a value label that matches the tracker.

        Qualitative values must be translated / mapped to how they appear in ResultItem.

        Args:
            * value_attr: the instance attribute that holds the result item value. (default: result_item_value)
        """
        if not value_attr:
            # default to attr name in result_item model
            value_attr = 'result_item_value'
        # get the value either with getattr or instance.get_result_value()
        if 'get_result_value' in dir(instance):
            result_value = instance.get_result_value(value_attr)
        else:
            try:
                result_value = getattr(instance, value_attr)
            except:
                raise TypeError('Expected attribute \'{0}\' or method \'get_result_value()\' on instance {0}.'.format(value_attr, instance._meta.object_name))
        # get a result value map, if it exists
        result_value_map = self._get_value_map(instance._meta.object_name.lower())
        if result_value_map:
            retval = result_value_map.get(result_value)
        else:
            retval = result_value
        # fail if there is no return value
        if not retval:
            raise ValueError('Tracker value cannot be None. Instance value is {0}, map={1}'.format(result_value, result_value_map))
        return retval

    def get_history(self, subject_identifier, value_datetime, order_desc=False):
        """Returns values from the history model for this subject as an ordered queryset
        filtered for records on or before value_datetime."""
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        self.update(subject_identifier)
        return HistoryModel.objects.filter(
            subject_identifier=subject_identifier,
            value_datetime__lte=value_datetime,
            test_key=self._get_group_name()).order_by(order_by)

    def get_current_value(self, subject_identifier, value_datetime):
        """Returns only the most current value."""
        queryset = self.get_history(subject_identifier, value_datetime, True)
        if queryset:
            return queryset[0].value
        else:
            return None

    def get_history_as_list(self, subject_identifier):
        """Returns all values as a list in ascending chronological order."""
        queryset = self.get_history(subject_identifier, datetime.today())
        return [qs.value for qs in queryset]

    def get_history_as_string(self, subject_identifier, mapped=True):
        """Returns a subject's qualitative values joined as a string in ascending chronological order.

        If mapped is True and a display_map is defined, map is inverted and a string of values is generated from the map."""
        if not self._get_display_map():
            mapped = False
        retlst = []
        inv_display_map = {}
        lst = self.get_history_as_list(subject_identifier)
        if mapped:
            for k, v in self._get_display_map().iteritems():
                inv_display_map[v] = inv_display_map.get(v, [])
                inv_display_map[v].append(k)
        for l in lst:
            if mapped:
                retlst.append(inv_display_map[l][0].lower())
            else:
                retlst.append(l)
        return ''.join(retlst)
