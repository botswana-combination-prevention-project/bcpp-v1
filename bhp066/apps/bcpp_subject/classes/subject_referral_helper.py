from datetime import datetime

from apps.bcpp_household_member.models import EnrollmentChecklist
from apps.bcpp_lab.models import SubjectRequisition

from ..models import (SubjectConsent, HivResult, Pima, HivTestReview, ResidencyMobility,
                      Circumcision, HivCareAdherence, ReproductiveHealth, HivTestingHistory,
                      HivResultDocumentation)

from ..choices import REFERRAL_CODES


class SubjectReferralHelper(object):

    # class attribute is accessed by the signal to ensure any modifications are caught in the post_save signal
    models = {
              'circumcision': Circumcision,
              'enrollment_checklist': EnrollmentChecklist,
              'hiv_care_adherence': HivCareAdherence,
              'hiv_result': HivResult,
              'hiv_result_documentation': HivResultDocumentation,
              'hiv_test_review': HivTestReview,
              'hiv_testing_history': HivTestingHistory,
              'pima': Pima,
              'reproductive_health': ReproductiveHealth,
              'residency_mobility': ResidencyMobility,
              'subject_consent': SubjectConsent,
              'subject_requisition': SubjectRequisition,
              }

    def __init__(self, instance):
        self._circumcised = None
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
        self._enrollment_checklist_instance = None
        self._on_art = None
        self._pima_instance = None
        self._pregnant = None
        self._recorded_hiv_result = None
        self._recorded_hiv_result_date = None
        self._referral_clinic = None
        self._referral_code_list = []
        self._subject_consent_instance = None
        self._subject_referral = {}
        self._todays_cd4_result = None
        self._todays_cd4_result_datetime = None
        self._todays_hiv_result = None
        self._todays_hiv_result_datetime = None
        self._verbal_hiv_result = None
        self._vl_requisition_instance = None
        self._vl_sample_drawn_datetime = None
        self.instance = instance
        self.gender = self.instance.subject_visit.appointment.registered_subject.gender
        self.household_member = self.instance.subject_visit.household_member
        self.subject_visit = self.instance.subject_visit

    def __repr__(self):
        return 'SubjectReferralHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    @property
    def subject_referral(self):
        """Returns a dictionary of the attributes {name: value, ...} from this class that match, by name, field attributes in the SubjectReferral model."""
        if not self._subject_referral:
            self._subject_referral = {}
            for attr in self.instance.__dict__:
                if attr in dir(self) and not attr.startswith('_'):
                    self._subject_referral.update({attr: getattr(self, attr)})
        return self._subject_referral

    @property
    def referral_code_list(self):
        """Returns a list of referral codes by reviewing the conditions for referral.

        MASA-LO: On ARVs but CD4 is low. Requires action.
        MASA-HI: On ARVs, CD4 is high.
        MAMO-LO: Not on ARV, low CD4"""
        self._referral_code_list = []
        if not self.hiv_result:
            if self.gender == 'M':
                if self.circumcised == False:
                    self._referral_code_list.append('SMC-UNK')  # refer if status unknown or indeterminate
                elif self.circumcised == None:
                    self._referral_code_list.append('SMC?UNK')  # refer if status unknown or indeterminate
            elif self.pregnant:
                self._referral_code_list.append('UNK?-PR')
            else:
                self._referral_code_list.append('TST-HIV')
        else:
            if self.hiv_result == 'IND':
                self._referral_code_list.append('HIV-IND')
                if self.gender == 'M':
                    if not self.circumcised:
                        self._referral_code_list.append('SMC-IND')
                    elif self.circumcised == None:
                        self._referral_code_list.append('SMC?IND')
            elif self.hiv_result == 'NEG':
                if self.gender == 'F' and self.pregnant:  # only refer F if pregnant
                    self._referral_code_list.append('NEG!-PR')
                elif self.gender == 'M' and self.circumcised == False:  # only refer M if not circumcised
                    self._referral_code_list.append('SMC-NEG')
                elif self.gender == 'M' and self.circumcised == None:  # only refer M if not circumcised
                    self._referral_code_list.append('SMC?NEG')
            elif self.hiv_result == 'POS':
                if self.gender == 'F' and self.pregnant and self.on_art:
                    self._referral_code_list.append('POS!-AN') if self.new_pos else self._referral_code_list.append('POS#-AN')
                elif self.gender == 'F' and self.pregnant and not self.on_art:
                    self._referral_code_list.append('POS!-PR') if self.new_pos else self._referral_code_list.append('POS#-PR')
                elif not self.on_art:
                    if not self.cd4_result:
                        self._referral_code_list.append('TST-CD4')
                    elif self.cd4_result > 350:
                        self._referral_code_list.append('POS!-HI') if self.new_pos else self._referral_code_list.append('POS#-HI')
                    elif self.cd4_result <= 350:
                        self._referral_code_list.append('POS!-LO') if self.new_pos else self._referral_code_list.append('POS#-LO')
                elif self.on_art:
                    self._referral_code_list.append('MASA-CC')
                    if self.defaulter:
                        self._referral_code_list = ['MASA-DF' for item in self._referral_code_list if item == 'MASA-CC']
                    if self.pregnant:
                        self._referral_code_list = ['POS#-AN' for item in self._referral_code_list if item == 'MASA-CC']
            else:
                self._referral_code_list.append('TST-HIV')

        # refer if on art and known positive to get VL, and o get outsiders to transfer care
        # referal date is the next appointment date if on art

        if self._referral_code_list:
            self._referral_code_list = list(set((self._referral_code_list)))
            self._referral_code_list.sort()
            for code in self._referral_code_list:
                if code not in self.valid_referral_codes:
                    raise ValueError('{0} is not a valid referral code.'.format(code))
        return self._referral_code_list

    @property
    def referral_code(self):
        """Returns a string of referral codes as a join of the list of referral codes delimited by ","."""
        return ','.join(self.referral_code_list)

    @property
    def valid_referral_codes(self):
        return [code for code, _ in REFERRAL_CODES if not code == 'pending']

    @property
    def hiv_result(self):
        """Returns the hiv status considering today\'s result, the last documented result and a verbal result with or without indirect documentation.

        Last or verbal results are used only if the value is POS otherwise None."""
        if not self._hiv_result:
            self._hiv_result = (
                self.todays_hiv_result or
                (self.last_hiv_result if self.last_hiv_result == 'POS' else None) or
                (self.documented_verbal_hiv_result if self.documented_verbal_hiv_result == 'POS' else None) or
                (self.verbal_hiv_result if (self.verbal_hiv_result == 'POS' and (self.direct_hiv_documentation or self.indirect_hiv_documentation)) else None)
                )
        return self._hiv_result

    @property
    def hiv_result_datetime(self):
        """ """
        if not self._hiv_result_datetime:
            last_hiv_result_datetime = None
            if self.last_hiv_result_date:
                last_hiv_result_datetime = datetime(self.last_hiv_result_date.year, self.last_hiv_result_date.month, self.last_hiv_result_date.day)
            self._hiv_result_datetime = self.todays_hiv_result_datetime or last_hiv_result_datetime
        return self._hiv_result_datetime

    @property
    def new_pos(self):
        """Returns True if combination of documents and test history show POS.

        ...note: if the result is verbal without any documentation the subject will be tested today and if POS considered a new POS (POS!)."""
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
    def arv_documentation(self):
        try:
            arv_documentation = self.convert_to_nullboolean(self.hiv_care_adherence_instance.arv_evidence)
        except AttributeError:
            arv_documentation = None
        return arv_documentation

    @property
    def arv_clinic(self):
        try:
            clinic_receiving_from = self.hiv_care_adherence_instance.clinic_receiving_from
        except AttributeError:
            clinic_receiving_from = None
        return clinic_receiving_from

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
                self._documented_verbal_hiv_result_date = self.hiv_result_documentation_instance.result_date
            except AttributeError:
                self._documented_verbal_hiv_result_date = None
        return self._documented_verbal_hiv_result_date

    @property
    def circumcised(self):
        """Returns None if female otherwise True if circumcised or False if not."""
        if self.gender == 'M':
            try:
                circumcision_instance = self.models.get('circumcision').objects.get(subject_visit=self.subject_visit)
                self._circumcised = self.convert_to_nullboolean(circumcision_instance.circumcised)
            except self.models.get('circumcision').DoesNotExist:
                self._circumcised = None
        return self._circumcised

    @property
    def citizen(self):
        citizen = None
        try:
            citizen = self.enrollment_checklist_instance.citizen == 'Yes' and self.subject_consent_instance.identity is not None
        except AttributeError:
            citizen = None
        return citizen

    @property
    def citizen_spouse(self):
        citizen_spouse = None
        try:
            citizen_spouse = self.enrollment_checklist_instance.legal_marriage == 'Yes' and self.subject_consent_instance.identity is not None
        except AttributeError:
            citizen_spouse = None
        return citizen_spouse

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
        return True if (self.todays_hiv_result == 'POS' or self.recorded_hiv_result == 'POS') else False

    @property
    def indirect_hiv_documentation(self):
        """Returns True if there is a verbal result and hiv_testing_history.other_record is Yes, otherwise None (not False).

        hiv_testing_history.other_record or hiv_care_adherence.arv_evidence is indirect evidence of a previous "POS result" only."""

        try:
            self._indirect_hiv_documentation = True if (self.hiv_testing_history_instance.verbal_hiv_result == 'POS' and (self.hiv_testing_history_instance.other_record == 'Yes' or self.arv_documentation)) else None
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
    def next_arv_clinic_appointment_date(self):
        next_appointment_date = None
        try:
            next_appointment_date = self.hiv_care_adherence_instance.next_appointment_date
        except AttributeError:
            pass
        return next_appointment_date

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
    def part_time_resident(self):
        """Returns True if part_time_resident as stated on enrollment_checklist."""
        try:
            part_time_resident = self.convert_to_nullboolean(self.enrollment_checklist_instance.part_time_resident)
        except AttributeError:
            part_time_resident = None
        return part_time_resident

    @property
    def permanent_resident(self):
        """Returns True if permanent resident as stated on ResidencyMobility."""
        try:
            residency_mobility_instance = self.models.get('residency_mobility').objects.get(subject_visit=self.subject_visit)
            permanent_resident = self.convert_to_nullboolean(residency_mobility_instance.permanent_resident)
        except self.models.get('residency_mobility').DoesNotExist:
            permanent_resident = None
        return permanent_resident

    @property
    def pregnant(self):
        """Returns None if male otherwise True if pregnant or False if not."""
        if self.gender == 'F':
            if not self._pregnant:
                try:
                    reproductive_health = self.models.get('reproductive_health').objects.get(subject_visit=self.subject_visit)
                    self._pregnant = self.convert_to_nullboolean(reproductive_health.currently_pregnant)
                except self.models.get('reproductive_health').DoesNotExist:
                    self._pregnant = None
        return self._pregnant

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
    def referral_clinic(self):
        return self.instance.referral_clinic if self.instance.referral_clinic != 'OTHER' else self.instance.referral_clinic_other

    @property
    def tb_symptoms(self):
        """Returns the tb_symptoms list as a convenience.

        Not necessary for determining the referral code."""
        return self.instance.tb_symptoms

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
    def urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        return True if [code for code in self.referral_code_list if code in ['MASA-DF', 'POS!-LO', 'POS#-LO', 'POS#-AN', 'POS!-PR']] else False

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
    def enrollment_checklist_instance(self):
        if not self._enrollment_checklist_instance:
            #try:
            self._enrollment_checklist_instance = self.models.get('enrollment_checklist').objects.get(household_member=self.subject_visit.household_member)
            #except self.models.get('enrollment_checklist').DoesNotExist:
            #    self._enrollment_checklist_instance = None
        return self._enrollment_checklist_instance

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
    def subject_consent_instance(self):
        if not self._subject_consent_instance:
            try:
                self._subject_consent_instance = self.models.get('subject_consent').objects.get(household_member=self.household_member)
            except self.models.get('subject_consent').DoesNotExist:
                self._subject_consent_instance = None
        return self._subject_consent_instance

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
