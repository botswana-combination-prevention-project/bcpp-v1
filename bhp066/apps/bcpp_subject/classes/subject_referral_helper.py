from edc.subject.appointment.constants import DONE
from apps.bcpp_lab.models import SubjectRequisition

from ..models import (SubjectConsent, HivResult, Pima, HivTestReview, Cd4History, ResidencyMobility,
                      Circumcision, HivCareAdherence, ReproductiveHealth, HivTestingHistory)

from ..choices import REFERRAL_CODES
from _mysql import result


class SubjectReferralHelper(object):

    def __init__(self, instance):
        self.pregnant = instance.pregnant
        self.gender = self.instance.subject_visit.appointment.registered_subject.gender
        self.instance = instance
        self.household_member = self.instance.subject_visit.household_member
        self.subject_visit = self.instance.subject_visit
        self.hiv_result_datetime = None
        self.last_hiv_test_date = None  # the last documented result
        self.direct_documentation = None  # TODO: needed?
        self.indirect_hiv_documentation = None  # for verbal hiv result only, if has other record indicating HIV status
        self.cd4_result_datetime = None
        self.last_cd4_result_datetime = None
        self.vl_sample_datetime_drawn = None
        self.update()

    def __repr__(self):
        return 'SubjectReferralHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    @property
    def referral_code(self):
        """Reviews the conditions for referral and sets to the correct referral code.

        MASA-LO: On ARVs but CD4 is low. Requires action.
        MASA-HI: On ARVs, CD4 is high.
        MAMO-LO: Not on ARV, low CD4"""
        referral_code = None
        if not self.hiv_result:
            self.append_to_referral_code('TST-HIV')
            if self.gender == 'M' and not self.circumcised:
                self.append_to_referral_code('SMC-UNK')  # refer if status unknown or indeterminate
        else:
            if self.hiv_result == 'IND':
                self.append_to_referral_code('HIV-IND')
                if self.gender == 'M' and not self.circumcised:
                    self.append_to_referral_code('SMC-IND')  # refer if status unknown or indeterminate
            elif self.hiv_result == 'NEG':
                if self.gender == 'F' and self.pregnant:  # only refer F if pregnant
                    self.append_to_referral_code('NEG!-PR')
                elif self.gender == 'M' and not self.circumcised:  # only refer M if not circumcised
                    self.append_to_referral_code('SMC-NEG')
            if self.hiv_result == 'POS':
                if self.gender == 'F' and self.pregnant and self.on_art:
                    self.append_to_referral_code('POS!-AN') if self.indirect_hiv_documentation else self.append_to_referral_code('POS#-AN')
                elif self.gender == 'F' and self.pregnant and not self.on_art:
                    self.append_to_referral_code('POS!-PR') if self.indirect_hiv_documentation else self.append_to_referral_code('POS#-PR')
                elif not self.on_art:
                    if not self.cd4_result:
                        self.append_to_referral_code('TST-CD4')
                    elif self.cd4_result > 350:
                        self.append_to_referral_code('POS!-HI') if self.indirect_hiv_documentation else self.append_to_referral_code('POS#-HI')
                    elif self.cd4_result <= 350:
                        self.append_to_referral_code('POS!-LO') if self.indirect_hiv_documentation else self.append_to_referral_code('POS#-LO')
                elif self.on_art:
                    if self.is_defaulter():
                        self.append_to_referral_code('MASA-DF')
                    if self.pregnant:
                        self.append_to_referral_code('POS#-AN')
                    elif not self.cd4_result:
                        self.append_to_referral_code('MASA')
                    elif self.cd4_result > 350:
                        self.append_to_referral_code('ERROR')
                    elif self.cd4_result <= 350:
                        self.append_to_referral_code('ERROR')
#         if not referral_code:
#             raise TypeError('Expected referral code to be one of {0}. Got {1}'.format([item[0] for item in REFERRAL_CODES], referral_code))
        return referral_code

    def get_referral_codes_as_list(self):
        return [x for x in self.referral_code.split(',')]

    def append_to_referral_code(self, value):
        referral_codes = []
        if value:
            referral_codes = [value]
            if self.referral_code:
                referral_codes.extend([item for item in self.get_referral_codes_as_list() if item != value])
                referral_codes.append(value)
        referral_codes.sort()
        self.referral_code = ';'.join(referral_codes)

    @property
    def hiv_result(self):
        """Returns the hiv status considering today\'s result, the last documented result and a verbal result with or without indirect documentation."""
        return self.todays_hiv_result or self.last_hiv_result or self.verbal_hiv_result

    @property
    def hiv_result_datetime(self):
        """ """
        return self.hiv_result_datetime or self.last_hiv_test_date

    @property
    def todays_hiv_result(self):
        """Returns an hiv result from today's test, if it exists."""
        try:
            hiv_result = HivResult.objects.get(subject_visit=self.instance.subject_visit, hiv_result__in=['POS', 'NEG', 'IND'])
            result = hiv_result.hiv_result
            self.hiv_result_datetime = hiv_result.hiv_result_datetime
            self.direct_documentation = True
        except HivResult.DoesNotExist:
            result = None
            self.hiv_result_datetime = None
            self.direct_documentation = None
        return result

    @property
    def last_hiv_result(self):
        """Returns an hiv result based on the last documented result."""
        try:
            hiv_test_review = HivTestReview.objects.get(subject_visit=self.instance.subject_visit)
            result = hiv_test_review.recorded_hiv_result
            self.last_hiv_test_date = hiv_test_review.hiv_test_date
            self.direct_documentation = True
        except HivTestReview.DoesNotExist:
            result = None
            self.last_hiv_test_date = None
            self.direct_documentation = None
        return result

    @property
    def verbal_hiv_result(self):
        """Returns the hiv result given verbally by the respondent from HivTestingHistory."""
        try:
            hiv_testing_history = HivTestingHistory.objects.get(subject_visit=self.subject_visit, verbal_hiv_result__in=['POS', 'NEG', 'IND'])
            result = hiv_testing_history.verbal_hiv_result
        except HivResult.DoesNotExist:
            result = None
        return result

    @property
    def new_pos(self):
        """Returns True if tested today.

        ...note: if the result is verbal without any documentation the subject will be tested today and if POS considered a new POS (POS!)."""
        if self.todays_hiv_result:
            return True
        return False

    def direct_documentation(self):
        return True if (self.todays_hiv_result or self.last_hiv_result) else False

    def indirect_documentation(self):
        """Returns True if there is a verbal result and hiv_testing_history.other_record is Yes, otherwise None (not False).

        hiv_testing_history.other_record is evidence of a previous POS result only.

        ...note: a verbal result
                   1. without direct documentation (has_record) should trigger an HIV test.
                   2. with direct documentation (has_record) will be recorded as the last_hiv_result."""
        try:
            hiv_testing_history = HivTestingHistory.objects.get(subject_visit=self.subject_visit, verbal_hiv_result__in=['POS'])  # looking for other record of POS result only
            indirect_hiv_documentation = hiv_testing_history.other_record == 'Yes'
        except HivResult.DoesNotExist:
            indirect_hiv_documentation = None
        return indirect_hiv_documentation

    def citizen(self):
        citizen = False
        if SubjectConsent.objects.filter(household_member=self.household_member).exists():
            subject_consent = SubjectConsent.objects.get(household_member=self.household_member)
            if subject_consent.identity_type == 'OMANG':
                citizen = True
        return citizen

    @property
    def cd4_result(self):
        return self.todays_cd4_result or self.last_cd4_result

    @property
    def todays_cd4_result(self):
        try:
            pima = Pima.objects.get(subject_visit=self.subject_visit, pima_today='Yes')
            result = int(pima.cd4_value)
            self.cd4_result_datetime = pima.cd4_datetime
        except Pima.DoesNotExist:
            result = None
            self.cd4_result_datetime = None
        return result

    @property
    def last_cd4_result(self):
        try:
            cd4_history = Cd4History.objects.get(subject_visit=self.subject_visit)
            result = cd4_history.last_cd4_count
            self.last_cd4_test_date = cd4_history.last_cd4_drawn_date
        except Cd4History.DoesNotExist:
            result = None
            self.last_cd4_result_date = None
        return result

    @property
    def vl_sample_drawn(self):
        vl_sample_drawn = False
        self.vl_sample_datetime_drawn = None
        try:
            subject_requisition = SubjectRequisition.objects.get(subject_visit=self.instance.subject_visit, panel__name='viral load')
            if subject_requisition.is_drawn == 'Yes':
                vl_sample_drawn = True
                self.vl_sample_datetime_drawn = subject_requisition.drawn_datetime
        except SubjectRequisition.DoesNotExist:
            pass
        return vl_sample_drawn

    @property
    def resident(self):
        """Returns True if permanent resident as stated on ResidencyMobility."""
        try:
            residency_mobility = ResidencyMobility.objects.get(subject_visit=self.instance.subject_visit)
            resident = self.convert_to_nullboolean(residency_mobility.permanent_resident)
        except ResidencyMobility.DoesNotExist:
            resident = None
        return resident

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
        pregnant = None
        if self.gender == 'F':
            try:
                reproductive_health = ReproductiveHealth.objects.get(subject_visit=self.subject_visit)
                pregnant = self.convert_to_nullboolean(reproductive_health.currently_pregnant)
            except ReproductiveHealth.DoesNotExist:
                pass
        return pregnant

    @property
    def on_art(self):
        on_art = None
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            on_art = hiv_care_adherence.on_art()
        except HivCareAdherence.DoesNotExist:
            pass
        return on_art

    @property
    def clinic_receiving_from(self):
        clinic_receiving_from = None
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            clinic_receiving_from = hiv_care_adherence.get_clinic_receiving_from()
        except HivCareAdherence.DoesNotExist:
            pass
        return clinic_receiving_from

    @property
    def next_appointment_date(self):
        next_appointment_date = None
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            next_appointment_date = hiv_care_adherence.get_next_appointment_date()
        except HivCareAdherence.DoesNotExist:
            pass
        return next_appointment_date

    @property
    def defaulter(self):
        defaulter = None
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.instance.subject_visit)
            defaulter = hiv_care_adherence.defaulter()
        except HivCareAdherence.DoesNotExist:
            pass
        return defaulter

    @property
    def urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        urgent_referral = False
        urgent_referral_codes = ['MASA-DF', 'POS!-LO', 'POS#-LO']
        if [code for code in self.referral_codes_as_list() if code in urgent_referral_codes]:
            urgent_referral = True
        return urgent_referral

    def convert_to_nullboolean(self, yes_no_dwta):
        if str(yes_no_dwta) in ['True', 'False', 'None']:
            return yes_no_dwta
        if yes_no_dwta.lower() == 'no':
            return False
        elif yes_no_dwta.lower() == 'yes':
            return True
        else:
            return None
