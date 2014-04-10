from datetime import datetime

from apps.bcpp_lab.models import SubjectRequisition

from ..models import (HivResult, Pima, HivTestReview, HivCareAdherence, HivTestingHistory, HivResultDocumentation)


class SubjectStatusHelper(object):

    # class attribute is accessed by the signal to ensure any modifications are caught in the post_save signal
    models = {
              'hiv_care_adherence': HivCareAdherence,
              'hiv_result': HivResult,
              'hiv_result_documentation': HivResultDocumentation,
              'hiv_test_review': HivTestReview,
              'hiv_testing_history': HivTestingHistory,
              'pima': Pima,
              'subject_requisition': SubjectRequisition,
              }

    def __init__(self, visit_instance):
        self._defaulter = None
        self._documented_verbal_hiv_result = None
        self._documented_verbal_hiv_result_date = None
        self._hiv_care_adherence_instance = None
        self._hiv_result = None
        self._hiv_result_datetime = None
        self._hiv_result_documentation_instance = None
        self._hiv_result_instance = None
        self._hiv_test_review_instance = None
        self._hiv_testing_history_instance = None
        self._indirect_hiv_documentation = None
        self._last_hiv_result = None
        self._last_hiv_result_date = None
        self._on_art = None
        self._pima_instance = None
        self._recorded_hiv_result = None
        self._recorded_hiv_result_date = None
        self._todays_cd4_result = None
        self._todays_cd4_result_datetime = None
        self._todays_hiv_result = None
        self._todays_hiv_result_datetime = None
        self._verbal_hiv_result = None
        self._vl_requisition_instance = None
        self._vl_sample_drawn_datetime = None
        self.subject_visit = visit_instance

    def __repr__(self):
        return 'SubjectStatusHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    @property
    def hiv_result(self):
        """Returns the hiv status considering today\'s result, the last documented result and a verbal result."""
        if not self._hiv_result:
            self._hiv_result = (
                self.todays_hiv_result or
                (self.last_hiv_result if self.last_hiv_result == 'POS' else None) or
                (self.documented_verbal_hiv_result if self.documented_verbal_hiv_result == 'POS' else None) or
                (self.verbal_hiv_result if (self.verbal_hiv_result == 'POS' and ((self.direct_hiv_documentation and self.recorded_hiv_result == 'POS') or self.indirect_hiv_documentation)) else None)
                )
        return self._hiv_result

    @property
    def hiv_result_datetime(self):
        """Returns the oldest hiv result datetime based on last then today."""
        if not self._hiv_result_datetime:
            last_hiv_result_datetime = None
            if self.last_hiv_result_date:
                last_hiv_result_datetime = datetime(self.last_hiv_result_date.year, self.last_hiv_result_date.month, self.last_hiv_result_date.day)
            if self.hiv_result == 'POS':
                self._hiv_result_datetime = last_hiv_result_datetime if self.last_hiv_result == 'POS' else self.todays_hiv_result_datetime  # take earliest if POS
            else:
                self._hiv_result_datetime = self.todays_hiv_result_datetime or last_hiv_result_datetime  # take latest if not POS
        return self._hiv_result_datetime

    @property
    def new_pos(self):
        """Returns True if combination of documents and test history show POS."""
        if (self.todays_hiv_result == 'POS' and self.recorded_hiv_result == 'POS'):
            return False
        elif (self.todays_hiv_result == 'POS' and self.verbal_hiv_result == 'POS' and not self.indirect_hiv_documentation):
            return False
        elif (self.verbal_hiv_result == 'POS' and (self.direct_hiv_documentation or self.indirect_hiv_documentation)):
            return False
        elif (self.recorded_hiv_result == 'POS'):
            return False
        else:
            if self.todays_hiv_result == 'POS':  # you only have today's result and possibly an undocumented verbal_hiv_result
                return True
            else:
                return None  # may have no result or just an undocumented verbal_hiv_result, which is not enough information.

    @property
    def should_be_tested(self):
        #Returns true if there is enough evidence that the subject is HIV+ with supporting documentation.
        #result = self.hiv_result
        return self.hiv_result != 'POS'

    @property
    def cd4_required(self):
        #Anybody that does not should not be tested i.e HIV+ with enough evidence, then CD4/PIMA should be reuired.
        #Except when they are already on ART with evidence
        if self.on_art and self.arv_documentation:
            return False
        return not self.should_be_tested

    @property
    def arv_documentation(self):
        try:
            arv_documentation = self.convert_to_nullboolean(self.hiv_care_adherence_instance.arv_evidence)
        except AttributeError:
            arv_documentation = None
        return arv_documentation

    @property
    def cd4_result_datetime(self):
        return self.todays_cd4_result_datetime

    @property
    def documented_verbal_hiv_result(self):
        """Returns an hiv result based on the confirmation of the verbal result by documentation."""
        if not self._documented_verbal_hiv_result:
            try:
                self._documented_verbal_hiv_result = self.hiv_result_documentation_instance.result_recorded
            except AttributeError:
                self._documented_verbal_hiv_result = None
        return self._documented_verbal_hiv_result

    @property
    def documented_verbal_hiv_result_date(self):
        """Returns an hiv result based on the confirmation of the verbal result by documentation."""
        if not self._documented_verbal_hiv_result_date:
            try:
                self._documented_verbal_hiv_result_date = self.hiv_result_documentation_instance.result_date or self.hiv_care_adherence_instance.first_arv
            except AttributeError:
                self._documented_verbal_hiv_result_date = None
        return self._documented_verbal_hiv_result_date

    @property
    def cd4_result(self):
        return self.todays_cd4_result

    @property
    def defaulter(self):
        if not self._defaulter:
            try:
                self._defaulter = self.hiv_care_adherence_instance.defaulter
            except AttributeError:
                self._defaulter = None
        return self._defaulter

    @property
    def direct_hiv_documentation(self):
        return True if (self.recorded_hiv_result in ['POS', 'NEG']) else False

    @property
    def indirect_hiv_documentation(self):
        """Returns True if there is a verbal result and hiv_testing_history.other_record is Yes, otherwise None (not False).

        hiv_testing_history.other_record or hiv_care_adherence.arv_evidence is indirect evidence of a previous "POS result" only."""

        try:
            if self.verbal_hiv_result == 'POS':
                self._indirect_hiv_documentation = True if (self.hiv_testing_history_instance.other_record == 'Yes' or self.arv_documentation) else False
        except AttributeError:
            self._indirect_hiv_documentation = None
        return self._indirect_hiv_documentation

    @property
    def last_hiv_result(self):
        if not self._last_hiv_result:
            self._last_hiv_result = self.recorded_hiv_result or self.documented_verbal_hiv_result
        return self._last_hiv_result

    @property
    def last_hiv_result_date(self):
        if not self._last_hiv_result_date:
            self._last_hiv_result_date = self.recorded_hiv_result_date or self.documented_verbal_hiv_result_date
        return self._last_hiv_result_date

    @property
    def on_art(self):
        self._on_art = None
        if not self._on_art:
            try:
                self._on_art = self.hiv_care_adherence_instance.on_art  # yes, on_art, not on_arv
            except AttributeError:
                self._on_art = False
        return self._on_art

    @property
    def recorded_hiv_result(self):
        """Returns an hiv result based on the last documented result."""
        if not self._recorded_hiv_result:
            try:
                self._recorded_hiv_result = self.hiv_test_review_instance.recorded_hiv_result
            except AttributeError:
                self._recorded_hiv_result = None
        return self._recorded_hiv_result

    @property
    def recorded_hiv_result_date(self):
        """Returns an hiv result based on the last documented result."""
        if not self._recorded_hiv_result_date:
            try:
                self._recorded_hiv_result_date = self.hiv_test_review_instance.hiv_test_date
            except AttributeError:
                self._recorded_hiv_result_date = None
        return self._recorded_hiv_result_date

    @property
    def todays_cd4_result(self):
        if not self._todays_cd4_result:
            try:
                self._todays_cd4_result = int(self.pima_instance.cd4_value)
            except AttributeError:
                self._todays_cd4_result = None
        return self._todays_cd4_result

    @property
    def todays_cd4_result_datetime(self):
        if not self._todays_cd4_result_datetime:
            try:
                self._todays_cd4_result_datetime = self.pima_instance.cd4_datetime
            except AttributeError:
                self._todays_cd4_result_datetime = None
        return self._todays_cd4_result_datetime

    @property
    def todays_hiv_result(self):
        """Returns an hiv result from today's test, if it exists."""
        if not self._todays_hiv_result:
            try:
                self._todays_hiv_result = self.hiv_result_instance.hiv_result
            except AttributeError:
                self._todays_hiv_result = None
        return self._todays_hiv_result

    @property
    def todays_hiv_result_datetime(self):
        """Returns an hiv result from today's test, if it exists."""
        if not self._todays_hiv_result_datetime:
            try:
                self._todays_hiv_result_datetime = self.hiv_result_instance.hiv_result_datetime
            except AttributeError:
                self._todays_hiv_result_datetime = None
        return self._todays_hiv_result_datetime

    @property
    def verbal_hiv_result(self):
        """Returns the hiv result given verbally by the respondent from HivTestingHistory."""
        if not self._verbal_hiv_result:
            try:
                self._verbal_hiv_result = self.hiv_testing_history_instance.verbal_hiv_result if self.hiv_testing_history_instance.verbal_hiv_result in ['POS', 'NEG', 'IND'] else None
            except AttributeError:
                self._verbal_hiv_result = None
        return self._verbal_hiv_result

    @property
    def vl_sample_drawn(self):
        return True if self.vl_requisition_instance else False

    @property
    def vl_sample_drawn_datetime(self):
        if not self._vl_sample_drawn_datetime:
            try:
                self._vl_sample_drawn_datetime = self.vl_requisition_instance.drawn_datetime
            except AttributeError:
                self._vl_sample_drawn_datetime = None
        return self._vl_sample_drawn_datetime

    @property
    def hiv_care_adherence_instance(self):
        if not self._hiv_care_adherence_instance:
            try:
                self._hiv_care_adherence_instance = self.models.get('hiv_care_adherence').objects.get(subject_visit=self.subject_visit)
            except self.models.get('hiv_care_adherence').DoesNotExist:
                self._hiv_care_adherence_instance = None
        return self._hiv_care_adherence_instance

    @property
    def hiv_result_instance(self):
        if not self._hiv_result_instance:
            try:
                self._hiv_result_instance = self.models.get('hiv_result').objects.get(subject_visit=self.subject_visit, hiv_result__in=['POS', 'NEG', 'IND'])
            except self.models.get('hiv_result').DoesNotExist:
                self._hiv_result_instance = None
        return self._hiv_result_instance

    @property
    def hiv_testing_history_instance(self):
        if not self._hiv_testing_history_instance:
            try:
                self._hiv_testing_history_instance = self.models.get('hiv_testing_history').objects.get(subject_visit=self.subject_visit)
            except self.models.get('hiv_testing_history').DoesNotExist:
                self._hiv_testing_history_instance = None
        return self._hiv_testing_history_instance

    @property
    def hiv_result_documentation_instance(self):
        if not self._hiv_result_documentation_instance:
            try:
                self._hiv_result_documentation_instance = self.models.get('hiv_result_documentation').objects.get(subject_visit=self.subject_visit, result_recorded__in=['POS', 'NEG', 'IND'])
            except self.models.get('hiv_result_documentation').DoesNotExist:
                self._hiv_result_documentation_instance = None
        return self._hiv_result_documentation_instance

    @property
    def hiv_test_review_instance(self):
        if not self._hiv_test_review_instance:
            try:
                self._hiv_test_review_instance = self.models.get('hiv_test_review').objects.get(subject_visit=self.subject_visit, recorded_hiv_result__in=['POS', 'NEG', 'IND'])
            except self.models.get('hiv_test_review').DoesNotExist:
                self._hiv_test_review_instance = None
        return self._hiv_test_review_instance

    @property
    def pima_instance(self):
        if not self._pima_instance:
            try:
                self._pima_instance = self.models.get('pima').objects.get(subject_visit=self.subject_visit, cd4_value__isnull=False)
            except self.models.get('pima').DoesNotExist:
                self._pima_instance = None
        return self._pima_instance

    @property
    def vl_requisition_instance(self):
        if not self._vl_requisition_instance:
            try:
                self._vl_requisition_instance = self.models.get('subject_requisition').objects.get(subject_visit=self.subject_visit, panel__name='Viral Load', is_drawn='Yes')
            except self.models.get('subject_requisition').DoesNotExist:
                pass
        return self._vl_requisition_instance

    def convert_to_nullboolean(self, yes_no_dwta):
        if str(yes_no_dwta) in ['True', 'False', 'None']:
            return yes_no_dwta
        if yes_no_dwta.lower() == 'no':
            return False
        elif yes_no_dwta.lower() == 'yes':
            return True
        else:
            return None
