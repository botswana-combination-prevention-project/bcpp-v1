from lab_clinic_api.models import ResultItem
from lab_longitudinal.models import HistoryModel


class History(object):

    def get_prep(self):
        """Returns a tuple of test_code, test_key where test_code may be a list.

        Users should override."""
        return (None, None)

    def update_prep(self, subject_identifier):
        """ Updates the LongitudinalHistoryModel if the user has other sources to include.

        Users may override."""
        pass

    def get(self, subject_identifier):
        self._update(subject_identifier)
        return [l.result for l in HistoryModel.objects.filter(subject_identifier=subject_identifier, test_key=self.test_key).order_by('result_datetime')]

    def _update(self, subject_identifier, test_key, test_code):
        test_code, test_key = self.get_prep()
        if not isinstance(test_code, list):
            test_code = [test_code]
        self.update_prep(subject_identifier)
        for result_item in ResultItem.objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=test_code):
            defaults = {'value': result_item.result}
            longitudinal_history_model, created = HistoryModel.objects.get_or_create(subject_identifier=subject_identifier,
                                                                                           test_key=test_key,
                                                                                           test_code=result_item.test_code.code,
                                                                                           value_datetime=result_item.assay_datetime,
                                                                                           defaults)
            if not created:
                if result_item.result:
                    longitudinal_history_model.value = result_item.result
                    longitudinal_history_model.save()
