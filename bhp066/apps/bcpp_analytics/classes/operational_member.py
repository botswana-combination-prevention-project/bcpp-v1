import collections
import datetime
from django.contrib.auth.models import User
from apps.bcpp.choices import COMMUNITIES, NOT_APPLICABLE
from apps.bcpp_household_member.constants import ABSENT, UNDECIDED, HTC_ELIGIBLE, HTC, REFUSED_HTC
from apps.bcpp_subject.models import (PositiveParticipant, HivResult, ElisaHivResult, HicEnrollment, SubjectConsent,
                                      SubjectReferral)
from apps.bcpp_household_member.models import HouseholdMember, EnrollmentLoss, SubjectRefusal

from .base_operational_report import BaseOperationalReport


class OperationalMember(BaseOperationalReport):

    def report_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        if self.survey.find('----') != -1:
            self.survey = ''

        self.date_to += datetime.timedelta(days=1)
        member = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                             user_modified__icontains=self.ra_username,
                                             household_structure__survey__survey_slug__icontains=self.survey)
        self.data_dict['1. Total household members'] = member.count()
        age_eligible_members = member.filter(eligible_member=True).count()
        self.data_dict['2. Total age eligible members'] = age_eligible_members
        not_age_eligible_members = member.filter(eligible_member=False, inability_to_participate=NOT_APPLICABLE).count()
        self.data_dict['3. Total members not eligible by age'] = not_age_eligible_members
        unable_to_participate_members = member.filter(eligible_member=False).exclude(inability_to_participate=NOT_APPLICABLE).count()
        self.data_dict['3. Total members unable to participate'] = unable_to_participate_members
        eligible_present_members = member.exclude(member_status=ABSENT).count()
        self.data_dict['6. Eligible present'] = eligible_present_members
        total_enrollment_loss = EnrollmentLoss.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                              modified__gte=self.date_from, modified__lte=self.date_to,
                                                              user_modified__icontains=self.ra_username,
                                                              household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['7. Total enrollment loss'] = total_enrollment_loss
        bhs_enrolled = member.filter(is_consented=True).count()
        self.data_dict['8. Total bhs enrolled'] = bhs_enrolled
        total_known_pos = PositiveParticipant.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                          created__gte=self.date_from,
                                                          created__lte=self.date_to,
                                                          user_created__icontains=self.ra_username,
                                                          subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['9. Known positive with documentation'] = total_known_pos
        total_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).exclude(hiv_result='Declined').exclude(hiv_result='Not performed').count()
        self.data_dict['91. Tested on filtering date'] = total_tested
        total_tested_negative = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='NEG',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['92. Tested and negative on filtering date'] = total_tested_negative
        total_elisa_negative = ElisaHivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='NEG',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['92. Tested and negative from ELISA on filtering date'] = total_elisa_negative
        total_tested_positive = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='POS',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['93. Tested and positive on filtering date'] = total_tested_positive
        total_elisa_positive = ElisaHivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='POS',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['94. Tested and negative from ELISA on filtering date'] = total_elisa_positive
        total_tested_indeterminate = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='IND',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['95. Tested and indeterminate on filtering date'] = total_tested_indeterminate
        total_tested_declined = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='Declined',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['96. Tested and declined on filtering date'] = total_tested_declined
        total_hic_enrolled = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hic_permission='Yes',
                                            subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).count()
        self.data_dict['97. Total HIC enrolled'] = total_hic_enrolled
        total_eligible_undecided = member.filter(eligible_member=True, member_status=UNDECIDED).count()
        self.data_dict['98. Total eligibles undecided'] = total_eligible_undecided
        total_eligible_refused = SubjectRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               survey__survey_slug__icontains=self.survey).count()
        self.data_dict['99. Total eligibles refused'] = total_eligible_refused
        total_eligible_absent = member.filter(eligible_member=True, member_status=ABSENT).count()
        self.data_dict['991. Total eligibles absent'] = total_eligible_absent
        total_consents = SubjectConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       survey__survey_slug__icontains=self.survey).count()
        self.data_dict['992. Total consents'] = total_consents
        total_consents_verified = SubjectConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               is_verified=True,
                                                               survey__survey_slug__icontains=self.survey).count()
        self.data_dict['993. Total consents verified'] = total_consents_verified
        total_hic_eligible = member.filter(eligible_member=True, member_status=HTC_ELIGIBLE).count()
        self.data_dict['994. Total HTC eligible'] = total_hic_eligible
        total_hic_accepted = member.filter(htc=True).count()
        self.data_dict['995. Total HTC accepted'] = total_hic_accepted
        total_hic_declined = member.filter(eligible_member=True, member_status=REFUSED_HTC).count()
        self.data_dict['996. Total HTC declined'] = total_hic_declined
        total_referrals = SubjectReferral.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                        created__gte=self.date_from,
                                                        created__lte=self.date_to,
                                                        user_created__icontains=self.ra_username,
                                                        subject_visit__household_member__household_structure__survey__survey_slug__icontains=self.survey).exclude(referral_code='NOT_REFERRED').count()
        self.data_dict['997. Referral codes generated'] = total_referrals
        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values