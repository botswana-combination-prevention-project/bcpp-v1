from apps.bcpp_lab.models import SubjectRequisition

from ..models import (SubjectConsent, HivResult, Pima, HivTestReview, Cd4History, ResidencyMobility,
                      Circumcision, HivCareAdherence, ReproductiveHealth)

from ..choices import REFERRAL_CODES


class SubjectReferralHelper(object):

    def __init__(self, instance):
        self._hiv_result = None
        self.instance = instance
        self.update()

    def __repr__(self):
        return 'SubjectReferralHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    def update(self):
        self.update_demographics()
        self.update_hiv()
        self.update_last_hiv_result()
        self.update_cd4()
        self.update_last_cd4()
        self.update_vl()
        self.update_residency()
        self.update_pregnant()
        self.update_circumcised()
        self.update_on_art()
        self.update_clinic_receiving_from()
        self.update_next_appointment_date()
        self.update_referral_code()
        self.update_urgent_referral()

    def update_referral_code(self):
        """Reviews the conditions for referral and sets to the correct referral code.

        MASA-LO: On ARVs but CD4 is low. Requires action.
        MASA-HI: On ARVs, CD4 is high.
        MAMO-LO: Not on ARV, low CD4"""
        self.instance.referral_code = None
        if not self.hiv_result:
            # refer for testing
            pass
        else:
            if self.hiv_result == 'IND':
                self.append_to_referral_code('HIV-IND')
            elif self.hiv_result == 'NEG' and self.instance.pregnant:
                self.append_to_referral_code('NEG!-PR')
            elif self.hiv_result == 'NEG' and self.instance.gender == 'F' and not self.instance.pregnant:
                self.append_to_referral_code(None)
            elif self.hiv_result == 'POS' and self.instance.pregnant and self.instance.on_art == True:
                self.append_to_referral_code('ERROR')  # TODO: POS#-AN  (hiv test was triggered by a verbal_result)
            elif self.hiv_result == 'POS' and self.instance.pregnant and self.instance.on_art == False:
                self.append_to_referral_code('POS!-PR')
            elif self.hiv_result == 'POS' and self.instance.pregnant and self.instance.on_art == None:
                self.append_to_referral_code('POS!-PR')
            elif self.hiv_result == 'NEG' and self.instance.circumcised == False:
                self.append_to_referral_code('SMC-NEG')
            elif self.hiv_result == 'POS':
                if self.instance.on_art == True or self.instance.on_art == False:
                    self.append_to_referral_code('ERROR')
                elif self.instance.on_art == None:
                    if not self.instance.cd4_result:
                        self.append_to_referral_code('TST-CD4')
                    elif self.instance.cd4_result > 350:
                        self.append_to_referral_code('POS!-HI')
                    elif self.instance.cd4_result <= 350:
                        self.append_to_referral_code('POS!-LO')
        elif self.instance.last_hiv_result == 'POS':
            if self.instance.is_defaulter():
                self.append_to_referral_code('MASA-DF')
            elif self.instance.on_art:
                if self.instance.pregnant:
                    self.append_to_referral_code('POS#-AN')
                elif not self.instance.cd4_result:
                    self.append_to_referral_code('MASA')
                elif self.instance.cd4_result > 350:
                    self.append_to_referral_code('ERROR')
                elif self.instance.cd4_result <= 350:
                    self.append_to_referral_code('ERROR')
            elif not self.instance.on_art:
                if self.instance.pregnant:
                    self.append_to_referral_code('POS#-PR')
                elif not self.instance.cd4_result:
                    self.append_to_referral_code('TST-CD4')
                elif self.instance.cd4_result > 350:
                    self.append_to_referral_code('POS#-HI')
                elif self.instance.cd4_result <= 350:
                    self.append_to_referral_code('POS#-LO')

        if self.instance.referral_code == 'ERROR' or not self.instance.referral_code:
            if self.instance.verbal_hiv_result == 'POS' or self.instance.other_record == 'Yes':
                if self.instance.on_art == None:
                
                if not self.instance.cd4_result:
                    self.append_to_referral_code('TST-CD4')
                elif self.instance.cd4_result > 350:
                    self.append_to_referral_code('POS!-HI')
                elif self.instance.cd4_result <= 350:
                    self.append_to_referral_code('POS!-LO')

                if self.instance.on_art == True:
                if self.instance.on_art == True:
            
            if self.instance.other_record == 'Yes' and self.instance.on_art == True:
                if not self.instance.cd4_result:
                    self.append_to_referral_code('TST-CD4')
                elif self.instance.cd4_result > 350:
                    self.append_to_referral_code('POS!-')
                elif self.instance.cd4_result <= 350:
                    self.append_to_referral_code('ERROR')
    
        # verbal pos/neg/unk and no document and not tested day - TST-HIV
        # verbal pos/neg/unk and no document and tested today - POS!
        # verbal pos/neg/unk and document pos - POS#

        if not self.instance.referral_code:
            self.append_to_referral_code('NOT-REF')
        if self.instance.referral_code not in [item[0] for item in REFERRAL_CODES]:
            raise TypeError('Expected referral code to be one of {0}. Got {1}'.format([item[0] for item in REFERRAL_CODES], self.instance.referral_code))

    @property
    def hiv_result(self):
        """ """
        if not self._hiv_result:
            self._hiv_result = self.update_hiv_result()
            if not self._hiv_result:
                self._hiv_result = self.update_last_hiv_result()
                if not self._hiv_result:
                    self._hiv_result = self.update_verbal_hiv_result()
        return self._hiv_result

    def update_demographics(self):
        self.instance.gender = self.instance.subject_visit.appointment.registered_subject.gender
        if SubjectConsent.objects.filter(household_member=self.instance.subject_visit.household_member).exists():
            subject_consent = SubjectConsent.objects.get(household_member=self.instance.subject_visit.household_member)
            if subject_consent.identity_type == 'OMANG':
                self.instance.citizen = True

    def update_hiv_result(self):
        if HivResult.objects.filter(subject_visit=self.instance.subject_visit, hiv_result__in=['POS', 'NEG', 'IND']).exists():
            hiv_result = HivResult.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.hiv_result = hiv_result.hiv_result
            self.instance.hiv_resultt_datetime = hiv_result.hiv_result_datetime
            if self.instance.hiv_result == 'POS':
                self.instance.new_pos = True
            elif self.instance.hiv_result == 'NEG':
                self.instance.new_pos = False
        else:
            self.instance.hiv_result = None
            self.instance.hiv_result_datetime = None
            self.instance.new_pos = None
        return self.instance.hiv_result

    def update_cd4(self):
        if Pima.objects.filter(subject_visit=self.instance.subject_visit, pima_today='Yes').exists():
            pima = Pima.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.cd4_result = int(pima.cd4_value)
            self.instance.cd4_result_datetime = pima.cd4_datetime
        else:
            self.instance.cd4_result = None
            self.instance.cd4_result_datetime = None

    def update_last_hiv_result(self):
        if HivTestReview.objects.filter(subject_visit=self.instance.subject_visit).exists():
            hiv_test_review = HivTestReview.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.last_hiv_result = hiv_test_review.recorded_hiv_result
            self.instance.last_hiv_test_date = hiv_test_review.hiv_test_date
            self.instance.new_pos = False
        else:
            self.instance.last_hiv_result = None
            self.instance.last_hiv_test_date = None
            self.instance.new_pos = None

    def update_last_cd4(self):
        if Cd4History.objects.filter(subject_visit=self.instance.subject_visit).exists():
            cd4_history = Cd4History.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.last_cd4_result = cd4_history.last_cd4_count
            self.instance.last_cd4_test_date = cd4_history.last_cd4_drawn_date
        else:
            self.instance.last_cd4_result = None
            self.instance.last_cd4_test_date = None

    def update_verbal_hiv_result(self):
        if HivTestingHistory.objects.filter(subject_visit=self.instance.subject_visit, verbal_hiv_result__in=['POS', 'NEG', 'IND']).exists():
            hiv_result = HivResult.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.hiv_result = hiv_result.hiv_result
            self.instance.hiv_resultt_datetime = hiv_result.hiv_result_datetime
            if self.instance.hiv_result == 'POS':
                self.instance.new_pos = True
            elif self.instance.hiv_result == 'NEG':
                self.instance.new_pos = False
        else:
            self.instance.hiv_result = None
            self.instance.hiv_result_datetime = None
            self.instance.new_pos = None
        return self.instance.hiv_result

    def update_vl(self):
        if SubjectRequisition.objects.filter(subject_visit=self.instance.subject_visit, panel__name='viral load').exists():
            if SubjectRequisition.objects.filter(subject_visit=self.instance.subject_visit, panel__name='viral load').count() > 1:
                #  FIXME: should not be possible, but dashboard still allows this (more than one req.per visit)
                subject_requisition = SubjectRequisition.objects.filter(subject_visit=self.instance.subject_visit, panel__name='viral load').order_by('created')[0]
            else:
                subject_requisition = SubjectRequisition.objects.get(subject_visit=self.instance.subject_visit, panel__name='viral load')
            if subject_requisition.is_drawn == 'Yes':
                self.instance.vl_sample_drawn = True
                self.instance.vl_sample_datetime_drawn = subject_requisition.drawn_datetime
            else:
                self.instance.vl_sample_drawn = False
                self.instance.vl_sample_datetime_drawn = None

    def update_residency(self):
        if ResidencyMobility.objects.filter(subject_visit=self.instance.subject_visit).exists():
            residency_mobility = ResidencyMobility.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.permanent_resident = self.instance.convert_to_nullboolean(residency_mobility.permanent_resident)
            self.instance.intend_residency = self.instance.convert_to_nullboolean(residency_mobility.intend_residency)
        else:
            self.instance.permanent_resident = None
            self.instance.intend_residency = None

    def update_circumcised(self):
        if self.instance.gender == 'M':
            if Circumcision.objects.filter(subject_visit=self.instance.subject_visit, circumcised='Yes').exists():
                self.instance.circumcised = True
            elif Circumcision.objects.filter(subject_visit=self.instance.subject_visit, circumcised='No').exists():
                self.instance.circumcised = False
        else:
            self.instance.circumcised = None

    def update_pregnant(self):
        if self.instance.gender == 'F':
            if ReproductiveHealth.objects.filter(subject_visit=self.instance.subject_visit).exists():
                reproductive_health = ReproductiveHealth.objects.get(subject_visit=self.instance.subject_visit)
                if reproductive_health.currently_pregnant == 'Yes':
                    self.instance.pregnant = True
                if reproductive_health.currently_pregnant == 'No':
                    self.instance.pregnant = False
        else:
            self.instance.pregnant = None

    def update_on_art(self):
        if HivCareAdherence.objects.filter(subject_visit=self.instance.subject_visit).exists():
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.on_art = hiv_care_adherence.on_art()
        else:
            self.instance.on_art = None

    def update_clinic_receiving_from(self):
        if HivCareAdherence.objects.filter(subject_visit=self.instance.subject_visit).exists():
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.clinic_receiving_from = hiv_care_adherence.get_clinic_receiving_from()
        else:
            self.instance.clinic_receiving_from = None

    def update_next_appointment_date(self):
        if HivCareAdherence.objects.filter(subject_visit=self.instance.subject_visit).exists():
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.instance.subject_visit)
            self.instance.next_appointment_date = hiv_care_adherence.get_next_appointment_date()
        else:
            self.instance.next_appointment_date = None

    def is_defaulter(self):
        if HivCareAdherence.objects.filter(subject_visit=self.instance.subject_visit).exists():
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.instance.subject_visit)
            return hiv_care_adherence.defaulter()
        return False

    def update_urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        urgent_referral = False
        urgent_referral_codes = ['MASA-DF', 'POS!-LO', 'POS#-LO']
        if [code for code in self.get_referral_codes_as_list() if code in urgent_referral_codes]:
            urgent_referral = True
        self.instance.urgent_referral = urgent_referral

    def get_referral_codes_as_list(self):
        return [x for x in self.instance.referral_code.split(',')]

    def append_to_referral_code(self, value):
        referral_codes = []
        if value:
            referral_codes = [value]
            if self.instance.referral_code:
                referral_codes.extend([item for item in self.get_referral_codes_as_list() if item != value])
                referral_codes.append(value)
        referral_codes.sort()
        self.instance.referral_code = ';'.join(referral_codes)

    def convert_to_nullboolean(self, yes_no_dwta):
        if str(yes_no_dwta) in ['True', 'False', 'None']:
            return yes_no_dwta
        if yes_no_dwta.lower() == 'no':
            return False
        elif yes_no_dwta.lower() == 'yes':
            return True
        else:
            return None
