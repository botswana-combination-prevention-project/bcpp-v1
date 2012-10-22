from django.core.exceptions import ImproperlyConfigured
from lab_clinic_api.models import ResultItem
from bhp_lab_tracker.models import HistoryModel


class LabTracker(object):

    def __init__(self):
        pass

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
        if not model_name in [model._meta.object_name.lower() for model in self.models]:
            raise ImproperlyConfigured('Model {0} has not been registered to this lab tracker.'.format(model_name))
        return self.get_value_map_prep(model_name)

    def get_value_map_prep(self, model_name):
        """Users should override to use a custom map for a given tracker model."""
        return {}

    def update(self, subject_identifier):
        """Updates the HistoryModel with the subject's values found in all the tracker models and ResultItem."""
        self._update_from_tracker_models(subject_identifier)
        self._update_from_result_item(subject_identifier)

    def update_with_tracker_instance(self, instance):
        """Updates the history model given a tracker model instance.

        Note that the tracker model must define the get_*** methods below.
        """
        self._update_history_model(
            instance._meta.object_name.lower(),
            instance.get_subject_identifier(),
            self._get_tracker_test_code(),
            self._get_tracker_result_value(instance),
            instance.get_result_datetime(),
            )

    def _update_from_tracker_models(self, subject_identifier):
        from bhp_visit_tracking.classes import VisitModelHelper

        for model in self.models:
            visit_field = VisitModelHelper().get_fieldname_from_cls(model)
            options = {'{visit_field}__appointment__registered_subject__subject_identifier'.format(visit_field=VisitModelHelper().get_fieldname_from_cls(model)): subject_identifier}
            #options = {'registered_subject__subject_identifier': subject_identifier}
            queryset = model.objects.filter(**options)
            #except:
            #    AttributeError('Lab Tracker model {0} must have a key to either a visit model or RegisteredSubject'.format(model._meta.object_name))
            for instance in queryset:
                self.update_with_tracker_instance(instance)

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
            history_model.save()

    def _update_from_result_item(self, subject_identifier):
        """Updates the history model from values in ResultItem for this subject."""
        for result_item in ResultItem.objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=self._get_resultitem_test_codes()):
            self._update_history_model('resultitem', subject_identifier, result_item.test_code.code, result_item.result_item_value, result_item.result_item_datetime)

    def _get_resultitem_test_code(self):
        """Returns a tuple of test codes that appear in ResultItem and are of interest to this tracker."""
        if not self.resultitem_test_code:
            raise AttributeError('Class attribute \'resultitem_test_code\' cannot be None. Should be a test code or tuple of test codes.')
        if not isinstance(self.resultitem_test_code, (list, tuple)):
            self.resultitem_test_code = (self.resultitem_test_code, )
        return self.resultitem_test_code

    def _get_tracker_test_code(self):
        if not self.tracker_test_code:
            raise AttributeError('Class attribute \'tracker_test_code\' cannot be None. Should be the test code used for tracker model results')
        return self.tracker_test_code

    def _get_group_name(self):
        """Returns a group_name or 'name' to group values in the history model for this class."""
        return self.group_name

    def _get_tracker_result_value(self, instance):
        """Returns a value mapped for the tracker model if a map exists.

        Qualitative values must be translated to how they appear in ResultItem."""
        result_value_map = self._get_value_map(instance._meta.object_name.lower())
        if result_value_map:
            retval = result_value_map.get(instance.get_result_value())
        else:
            retval = instance.get_result_value()
        if not retval:
            raise ValueError('Tracker value cannot be None. Instance value is {0}, map={1}'.format(instance.get_result_value(), result_value_map))
        return retval

    def get_history(self, subject_identifier, order_desc=False):
        """Returns all values in the history model for this subject as an ordered queryset."""
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        self.update(subject_identifier)
        return HistoryModel.objects.filter(subject_identifier=subject_identifier, test_key=self._get_group_name()).order_by(order_by)

    def get_current_value(self, subject_identifier):
        """Returns only the most current value."""
        queryset = self.get_history(subject_identifier, True)
        if queryset:
            return queryset[0].value
        else:
            return None

    def get_history_as_list(self, subject_identifier):
        """Returns all values as a list in ascending chronological order."""
        queryset = self.get_history(subject_identifier)
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
