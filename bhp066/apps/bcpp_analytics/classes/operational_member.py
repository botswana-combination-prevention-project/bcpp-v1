import collections
import datetime
from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities
from apps.bcpp.choices import COMMUNITIES, NOT_APPLICABLE
from apps.bcpp_household_member.constants import ABSENT, UNDECIDED, HTC_ELIGIBLE, HTC, REFUSED_HTC
from apps.bcpp_subject.models import (PositiveParticipant, HivResult, ElisaHivResult, HicEnrollment, SubjectConsent,
                                      SubjectReferral)
from apps.bcpp_household_member.models import HouseholdMember, EnrollmentLoss, SubjectRefusal


class OperationalMember():

    def __init__(self, request):
        self.member_info = {}
        self.utilities = OperationalReportUtilities()
        self.date_from = self.utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
        self.date_to = self.utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')
        self.ra_username = request.GET.get('ra', '')
        self.community = request.GET.get('community', '')
        self.previous_ra = self.ra_username
        self.previous_community = self.community
        self.communities = None
        self.ra_usernames = None

#     def operational_plots(self):
#         pass

    def return_communities(self):
        return self.communities

    def return_ra_usernames(self):
        return self.ra_usernames

    def return_member_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        member = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                             user_modified__icontains=self.ra_username)
        self.member_info['1. Total household members'] = member.count()
        age_eligible_members = member.filter(eligible_member=True).count()
        self.member_info['2. Total age eligible members'] = age_eligible_members
        not_age_eligible_members = member.filter(eligible_member=False, inability_to_participate=NOT_APPLICABLE).count()
        self.member_info['3. Total members not eligible by age'] = not_age_eligible_members
        unable_to_participate_members = member.filter(eligible_member=False).exclude(inability_to_participate=NOT_APPLICABLE).count()
        self.member_info['3. Total members unable to participate'] = unable_to_participate_members
        eligible_present_members = member.exclude(member_status=ABSENT).count()
        self.member_info['6. Eligible present'] = eligible_present_members
        total_enrollment_loss = EnrollmentLoss.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                              modified__gte=self.date_from, modified__lte=self.date_to,
                                                              user_modified__icontains=self.ra_username).count()
        self.member_info['7. Total enrollment loss'] = total_enrollment_loss
        bhs_enrolled = member.filter(is_consented=True).count()
        self.member_info['8. Total bhs enrolled'] = bhs_enrolled
        total_known_pos = PositiveParticipant.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                          created__gte=self.date_from,
                                                          created__lte=self.date_to,
                                                          user_created__icontains=self.ra_username).count()
        self.member_info['9. Known positive with documentation'] = total_known_pos
        total_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username).exclude(hiv_result='Declined').exclude(hiv_result='Not performed').count()
        self.member_info['91. Tested on filtering date'] = total_tested
        total_tested_negative = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='NEG').count()
        self.member_info['92. Tested and negative on filtering date'] = total_tested_negative
        total_elisa_negative = ElisaHivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='NEG').count()
        self.member_info['92. Tested and negative from ELISA on filtering date'] = total_elisa_negative
        total_tested_positive = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='POS').count()
        self.member_info['93. Tested and positive on filtering date'] = total_tested_positive
        total_elisa_positive = ElisaHivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='POS').count()
        self.member_info['94. Tested and negative from ELISA on filtering date'] = total_elisa_positive
        total_tested_indeterminate = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='IND').count()
        self.member_info['95. Tested and indeterminate on filtering date'] = total_tested_indeterminate
        total_tested_declined = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='Declined').count()
        self.member_info['96. Tested and declined on filtering date'] = total_tested_declined
        total_hic_enrolled = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hic_permission='Yes').count()
        self.member_info['97. Total HIC enrolled'] = total_hic_enrolled
        total_eligible_undecided = member.filter(eligible_member=True, member_status=UNDECIDED).count()
        self.member_info['98. Total eligibles undecided'] = total_eligible_undecided
        total_eligible_refused = SubjectRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username).count()
        self.member_info['99. Total eligibles refused'] = total_eligible_refused
        total_eligible_absent = member.filter(eligible_member=True, member_status=ABSENT).count()
        self.member_info['991. Total eligibles absent'] = total_eligible_absent
        total_consents = SubjectConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username).count()
        self.member_info['992. Total consents'] = total_consents
        total_consents_verified = SubjectConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               is_verified=True).count()
        self.member_info['993. Total consents verified'] = total_consents_verified
        total_hic_eligible = member.filter(eligible_member=True, member_status=HTC_ELIGIBLE).count()
        self.member_info['994. Total HTC eligible'] = total_hic_eligible
        total_hic_accepted = member.filter(eligible_member=True, member_status=HTC).count()
        self.member_info['995. Total HTC accepted'] = total_hic_accepted
        total_hic_declined = member.filter(eligible_member=True, member_status=REFUSED_HTC).count()
        self.member_info['996. Total HTC declined'] = total_hic_declined
        total_referrals = SubjectReferral.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                        created__gte=self.date_from,
                                                        created__lte=self.date_to,
                                                        user_created__icontains=self.ra_username).exclude(referral_code='NOT_REFERRED').count()
        self.member_info['997. Referral codes generated'] = total_referrals

        values = collections.OrderedDict(sorted(self.member_info.items()))
        communities = []
        if (self.previous_community.find('----') == -1) and (not self.previous_community == ''):  # Passing filtered results
            # communities = [community[0].lower() for community in  COMMUNITIES]
            for community in  COMMUNITIES:
                if community[0].lower() != self.previous_community:
                    communities.append(community[0])
            communities.insert(0, self.previous_community)
            communities.insert(1, '---------')
        else:
            communities = [community[0].lower() for community in  COMMUNITIES]
            communities.insert(0, '---------')
        self.communities = communities
        ra_usernames = []
        if (self.previous_ra.find('----') == -1) and (not self.previous_ra == ''):
            for ra_name in [user.username for user in User.objects.filter(groups__name='field_research_assistant')]:
                if ra_name != self.previous_ra:
                    ra_usernames.append(ra_name)
            ra_usernames.insert(0, self.previous_ra)
            ra_usernames.insert(1, '---------')
        else:
            ra_usernames = [user.username for user in User.objects.filter(groups__name='field_research_assistant')]
            ra_usernames.insert(0, '---------')
        self.ra_usernames = ra_usernames
        return values