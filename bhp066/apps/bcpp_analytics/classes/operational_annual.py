import collections
import datetime
from edc.constants import DEAD

from apps.bcpp_survey.models import Survey
from apps.bcpp_household_member.constants import ABSENT, HTC_ELIGIBLE, HTC, BHS_SCREEN, ANNUAL, NOT_ELIGIBLE
from apps.bcpp_subject.models import (HivResult, HicEnrollment)
from apps.bcpp_household_member.models import HouseholdMember, SubjectRefusal

from .base_operational_report import BaseOperationalReport


class OperationalAnnual(BaseOperationalReport):

    def report_data(self):
        # DEFINITIONS
        # annual_member: All members created in baseline survey household structures.
        # targeted_members:  All members created in baseline survey household structures and consented only.
        # new_members: Members that got newly created in the annual survey i.e they did not exist in the baseline survey.
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        current_annual_survey = (Survey.objects.current_survey() if Survey.objects.current_survey().survey_slug != 'bcpp_year_1' else Survey.objects.next_survey())
        previous_survey = Survey.objects.previous_survey()
        annual_member = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                             household_structure__survey=previous_survey,
                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                             user_modified__icontains=self.ra_username)
        annual_internal_identifiers = [mem.internal_identifier for mem in annual_member]
        targeted_members = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                             household_structure__survey=previous_survey,
                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                             user_modified__icontains=self.ra_username,
                                             is_consented=True)
        targeted_members_internal_identifiers = [mem.internal_identifier for mem in targeted_members]
        new_members = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                             household_structure__survey=current_annual_survey,
                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                             user_modified__icontains=self.ra_username).exclude(internal_identifier__in=annual_internal_identifiers)
        new_member_internal_indentifiers = [mem.internal_identifier for mem in new_members]
        self.data_dict['1. Targeted BHS only members'] = targeted_members.count()
        annual_members_reached = annual_member.exclude(member_status=ABSENT).count()
        self.data_dict['2. Annual BHS only members reached'] = annual_members_reached
        targeted_members_unreached = targeted_members.filter(member_status=ANNUAL).count()
        self.data_dict['3. Targeted BHS only members not reached'] = targeted_members_unreached
        targeted_members_relocated = targeted_members.filter(eligible_member=True).count()
        self.data_dict['4. Targeted BHS only members that relocated'] = 'N/A'
        targeted_members_deceased = targeted_members.filter(survival_status=DEAD).count()
        self.data_dict['5. Targeted BHS only members are now deceased'] = targeted_members_deceased
        targeted_members_incarcerated = targeted_members.filter(eligible_member=True).count()
        self.data_dict['6. Targeted BHS only members are now incarcerated'] = 'N/A'
        targeted_eligible_retesting = 'N/A'
        self.data_dict['7. Targeted BHS members eligible for re-testing'] = targeted_eligible_retesting
        targeted_members_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=targeted_members_internal_identifiers,
                                            subject_visit__household_member__household_structure__survey=current_annual_survey,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username).exclude(hiv_result='Declined').exclude(hiv_result='Not performed').count()
        self.data_dict['8. Targeted BHS members that tested'] = targeted_members_tested
        annual_declined_testing = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=targeted_members_internal_identifiers,
                                            subject_visit__household_member__household_structure__survey=current_annual_survey,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hiv_result='Declined').count()
        self.data_dict['9. Targeted BHS members that declined testing'] = annual_declined_testing
        annual_new_hic_eligible = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=annual_internal_identifiers,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username).exclude(subject_visit__household_member__internal_identifier__in=targeted_members_internal_identifiers).count()
        self.data_dict['91. Annual BHS members newly eligible for HIC'] = annual_new_hic_eligible
        annual_new_hic_enrolled = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=annual_internal_identifiers,
                                            created__gte=self.date_from,
                                            created__lte=self.date_to,
                                            user_created__icontains=self.ra_username,
                                            hic_permission='Yes').exclude(subject_visit__household_member__internal_identifier__in=targeted_members_internal_identifiers).count()
        self.data_dict['92. Annual BHS members newly eligible for HIC that enrolled'] = annual_new_hic_enrolled
        self.data_dict['93. New members identified'] = new_members.count()
        new_consented = new_members.filter(is_consented=True).count()
        self.data_dict['94. New members consented'] = new_consented
        #self.data_dict['94. Statuses for new members that DID not consent'] = new_members.values('member_status').annotate(dcount=Count('member_status'))
        new_hic_eligible = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=new_member_internal_indentifiers).count()
        self.data_dict['95. New members eligible for HIC'] = new_hic_eligible
        new_hic = HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                            subject_visit__household_member__internal_identifier__in=new_member_internal_indentifiers,
                                            hic_permission='Yes').count()
        self.data_dict['96. New members that enrolled in HIC'] = new_hic
        new_bhs_screen = new_members.filter(member_status=BHS_SCREEN).count()
        self.data_dict['97. New members BHS SCREEN'] = new_bhs_screen
        new_htc_eligible = new_members.filter(member_status=HTC_ELIGIBLE).count()
        self.data_dict['98. New members HTC ELIGIBLE'] = new_htc_eligible
        new_htc = new_members.filter(member_status=HTC).count()
        self.data_dict['99. New members HTC only'] = new_htc
        new_absent = new_members.filter(member_status=ABSENT).count()
        self.data_dict['991. New members ABSENT'] = new_absent
        new_not_eligible = new_members.filter(member_status=NOT_ELIGIBLE).count()
        self.data_dict['992. New members NOT ELIGIBLE for BHS'] = new_not_eligible
        new_refused = SubjectRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                    household_member__internal_identifier__in=new_member_internal_indentifiers).count()
        self.data_dict['993. New members that refused'] = new_refused

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values