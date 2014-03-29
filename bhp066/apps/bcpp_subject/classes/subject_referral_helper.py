from datetime import datetime

from apps.bcpp_household_member.models import EnrollmentChecklist
from apps.bcpp_lab.models import SubjectRequisition

from ..models import (SubjectConsent, HivResult, Pima, HivTestReview, ResidencyMobility,
                      Circumcision, HivCareAdherence, ReproductiveHealth, HivTestingHistory,
                      HivResultDocumentation)


class SubjectReferralHelper(object):

    def __init__(self, instance):
        self._pregnant = None
        self._hiv_result = None
        self._hiv_result_datetime = None
        self._defaulter = None
        self._documented_verbal_hiv_result = None
        self._documented_verbal_hiv_result_date = None
        self._hiv_care_adherence_instance = None
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
        self._referral_clinic = None
        self._referral_code_list = []
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
    def cd4_result_datetime(self):
        return self.todays_cd4_result_datetime

    @property
    def referral_code_list(self):
        """Returns a list of referral codes by reviewing the conditions for referral.

        MASA-LO: On ARVs but CD4 is low. Requires action.
        MASA-HI: On ARVs, CD4 is high.
        MAMO-LO: Not on ARV, low CD4"""
        self._referral_code_list = []
        if not self.hiv_result:
            self._referral_code_list.append('TST-HIV')
            if self.gender == 'M' and not self.circumcised:
                self._referral_code_list.append('SMC-UNK')  # refer if status unknown or indeterminate
        else:
            if self.hiv_result == 'IND':
                self._referral_code_list.append('HIV-IND')
                if self.gender == 'M' and not self.circumcised:
                    self._referral_code_list.append('SMC-IND')  # refer if status unknown or indeterminate
            elif self.hiv_result == 'NEG':
                if self.gender == 'F' and self.pregnant:  # only refer F if pregnant
                    self._referral_code_list.append('NEG!-PR')
                elif self.gender == 'M' and not self.circumcised:  # only refer M if not circumcised
                    self._referral_code_list.append('SMC-NEG')
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
                    self._referral_code_list.append('MASA')
                    if self.defaulter:
                        self._referral_code_list = ['MASA-DF' for item in self._referral_code_list if item == 'MASA']
                    if self.pregnant:
                        self._referral_code_list = ['POS#-AN' for item in self._referral_code_list if item == 'MASA']
            else:
                self._referral_code_list.append('TST-HIV')

        # refer if on art and known positive to get VL, and o get outsiders to transfer care
        # referal date is the next appointment date if on art

        if self._referral_code_list:
            self._referral_code_list = list(set((self._referral_code_list)))
            self._referral_code_list.sort()
        return self._referral_code_list

    @property
    def referral_code(self):
        """Returns a string of referral codes as a join of the list of referral codes delimited by ","."""
        return ','.join(self.referral_code_list)

    @property
    def hiv_result(self):
        """Returns the hiv status considering today\'s result, the last documented result and a verbal result with or without indirect documentation."""
        if not self._hiv_result:
            self._hiv_result = self.todays_hiv_result or self.last_hiv_result or self.documented_verbal_hiv_result or (self.verbal_hiv_result if (self.verbal_hiv_result == 'POS' and (self.direct_hiv_documentation or self.indirect_hiv_documentation)) else None)
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
    def hiv_result_instance(self):
        if not self._hiv_result_instance:
            try:
                self._hiv_result_instance = HivResult.objects.get(subject_visit=self.subject_visit, hiv_result__in=['POS', 'NEG', 'IND'])
            except HivResult.DoesNotExist:
                self._hiv_result_instance = None
        return self._hiv_result_instance

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
    def hiv_test_review_instance(self):
        if not self._hiv_test_review_instance:
            try:
                self._hiv_test_review_instance = HivTestReview.objects.get(subject_visit=self.subject_visit, recorded_hiv_result__in=['POS', 'NEG', 'IND'])
            except HivTestReview.DoesNotExist:
                self._hiv_test_review_instance = None
        return self._hiv_test_review_instance

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
    def hiv_result_documentation_instance(self):
        if not self._hiv_result_documentation_instance:
            try:
                self._hiv_result_documentation_instance = HivResultDocumentation.objects.get(subject_visit=self.subject_visit, result_recorded__in=['POS', 'NEG', 'IND'])
            except HivResultDocumentation.DoesNotExist:
                self._hiv_result_documentation_instance = None
        return self._hiv_result_documentation_instance

    @property
    def documented_verbal_hiv_result(self):
        """Returns an hiv result based on the confirmation of the verbal result by documention."""
        if not self._documented_verbal_hiv_result:
            try:
                self._documented_verbal_hiv_result = self.hiv_result_documentation_instance.result_recorded
            except AttributeError:
                self._documented_verbal_hiv_result = None
        return self._documented_verbal_hiv_result

    @property
    def documented_verbal_hiv_result_date(self):
        """Returns an hiv result based on the confirmation of the verbal result by documention."""
        if not self._documented_verbal_hiv_result_date:
            try:
                self._documented_verbal_hiv_result_date = self.hiv_result_documentation_instance.result_date
            except AttributeError:
                self._documented_verbal_hiv_result_date = None
        return self._documented_verbal_hiv_result_date

    @property
    def hiv_testing_history_instance(self):
        if not self._hiv_testing_history_instance:
            try:
                self._hiv_testing_history_instance = HivTestingHistory.objects.get(subject_visit=self.subject_visit)
            except HivTestingHistory.DoesNotExist:
                self._hiv_testing_history_instance = None
        return self._hiv_testing_history_instance

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
            return True

    @property
    def direct_hiv_documentation(self):
        return True if (self.todays_hiv_result == 'POS' or self.recorded_hiv_result == 'POS') else False

    @property
    def indirect_hiv_documentation(self):
        """Returns True if there is a verbal result and hiv_testing_history.other_record is Yes, otherwise None (not False).

        hiv_testing_history.other_record is indirect evidence of a previous "POS result" only.

        ...note: a verbal result
                   1. without direct documentation (has_record) should trigger an HIV test.
                   2. with direct documentation (has_record) will be recorded as the last_hiv_result."""
        try:
            self._indirect_hiv_documentation = True if (self.hiv_testing_history_instance.verbal_hiv_result == 'POS' and self.hiv_testing_history_instance.other_record == 'Yes') else None
        except AttributeError:
            self._indirect_hiv_documentation = None
        return self._indirect_hiv_documentation

    @property
    def citizen(self):
        citizen = False
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(household_member=self.household_member)
            subject_consent = SubjectConsent.objects.get(household_member=self.household_member)
            if enrollment_checklist.citizen == 'Yes' and subject_consent.identity:
                citizen = True
        except EnrollmentChecklist.DoesNotExist:
            citizen = None
        except SubjectConsent.DoesNotExist:
            citizen = None
        return citizen

    @property
    def citizen_spouse(self):
        citizen_spouse = False
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(household_member=self.household_member)
            subject_consent = SubjectConsent.objects.get(household_member=self.household_member)
            if enrollment_checklist.legal_marriage == 'Yes' and subject_consent.identity:
                citizen_spouse = True
        except EnrollmentChecklist.DoesNotExist:
            citizen_spouse = None
        except SubjectConsent.DoesNotExist:
            citizen_spouse = None
        return citizen_spouse

    @property
    def cd4_result(self):
        return self.todays_cd4_result

    @property
    def pima_instance(self):
        if not self._pima_instance:
            try:
                self._pima_instance = Pima.objects.get(subject_visit=self.subject_visit, cd4_value__isnull=False)
            except Pima.DoesNotExist:
                self._pima_instance = None
        return self._pima_instance

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
    def vl_requisition_instance(self):
        if not self._vl_requisition_instance:
            try:
                self._vl_requisition_instance = SubjectRequisition.objects.get(subject_visit=self.subject_visit, panel__name='Viral Load', is_drawn='Yes')
            except SubjectRequisition.DoesNotExist:
                pass
        return self._vl_requisition_instance

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
    def permanent_resident(self):
        """Returns True if permanent resident as stated on ResidencyMobility."""
        try:
            residency_mobility = ResidencyMobility.objects.get(subject_visit=self.subject_visit)
            permanent_resident = self.convert_to_nullboolean(residency_mobility.permanent_resident)
        except ResidencyMobility.DoesNotExist:
            permanent_resident = None
        return permanent_resident

    @property
    def circumcised(self):
        """Returns None if female otherwise True if cirecumcised or False if not."""
        circumcised = None
        if self.gender == 'M':
            try:
                circumcision = Circumcision.objects.get(subject_visit=self.subject_visit)
                circumcised = self.convert_to_nullboolean(circumcision.circumcised)
            except Circumcision.DoesNotExist:
                pass
        return circumcised

    @property
    def pregnant(self):
        """Returns None if male otherwise True if pregnant or False if not."""
        if self.gender == 'F':
            if not self._pregnant:
                try:
                    reproductive_health = ReproductiveHealth.objects.get(subject_visit=self.subject_visit)
                    self._pregnant = self.convert_to_nullboolean(reproductive_health.currently_pregnant)
                except ReproductiveHealth.DoesNotExist:
                    self._pregnant = None
        return self._pregnant

    @property
    def hiv_care_adherence_instance(self):
        if not self._hiv_care_adherence_instance:
            try:
                self._hiv_care_adherence_instance = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            except HivCareAdherence.DoesNotExist:
                self._hiv_care_adherence_instance = None
        return self._hiv_care_adherence_instance

    @property
    def on_art(self):
        if not self._on_art:
            try:
                self._on_art = self.hiv_care_adherence_instance.on_art
            except AttributeError:
                self._on_art = None
        return self._on_art

    @property
    def art_documentation(self):
        try:
            art_documentation = self.hiv_care_adherence_instance.arv_evidence == 'Yes'
        except AttributeError:
            art_documentation = None
        return art_documentation

    @property
    def current_arv_clinic(self):
        clinic_receiving_from = None
        try:
            clinic_receiving_from = self.hiv_care_adherence_instance.clinic_receiving_from
        except AttributeError:
            pass
        return clinic_receiving_from

    @property
    def next_arv_clinic_appointment_date(self):
        next_appointment_date = None
        try:
            next_appointment_date = self.hiv_care_adherence_instance.next_appointment_date
        except AttributeError:
            pass
        return next_appointment_date

    @property
    def defaulter(self):
        if not self._defaulter:
            try:
                self._defaulter = self.hiv_care_adherence_instance.defaulter
            except AttributeError:
                self._defaulter = None
        return self._defaulter

    @property
    def tb_symptoms(self):
        """Returns the tb_symptoms list as a convenience.

        Not necessary for determining the referral code."""
        return self.instance.tb_symptoms

    @property
    def referral_clinic(self):
        return self.instance.referral_clinic if self.instance.referral_clinic != 'OTHER' else self.instance.referral_clinic_other

    @property
    def arv_clinic(self):
        return self.instance.arv_clinic

    @property
    def urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        return True if [code for code in self.referral_code_list if code in ['MASA-DF', 'POS!-LO', 'POS#-LO']] else False

    def convert_to_nullboolean(self, yes_no_dwta):
        if str(yes_no_dwta) in ['True', 'False', 'None']:
            return yes_no_dwta
        if yes_no_dwta.lower() == 'no':
            return False
        elif yes_no_dwta.lower() == 'yes':
            return True
        else:
            return None
