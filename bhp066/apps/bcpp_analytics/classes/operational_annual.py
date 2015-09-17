import collections
import datetime
import threading

from django.db.models import Q, Count

from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household_member.constants import (
    ABSENT, HTC_ELIGIBLE, HTC, BHS_SCREEN, ANNUAL, NOT_ELIGIBLE, UNDECIDED)
from bhp066.apps.bcpp_subject.models import (HivResult, HicEnrollment)
from bhp066.apps.bcpp_household_member.models import HouseholdMember, SubjectRefusal

from .base_operational_report import BaseOperationalReport


class OperationalAnnual(BaseOperationalReport):

    def report_data(self):
        """"DEFINITIONS
        annual_member: All members created in baseline survey household structures.
        targeted_members:  All members created in baseline survey household structures and consented only, and are now
                           in the annual survey.
        new_members: Members that got newly created in the annual survey i.e they did not exist in the baseline survey.
        """
        threads = []
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        current_annual_survey = (Survey.objects.current_survey() if Survey.objects.current_survey().survey_slug != 'bcpp_year_1' else Survey.objects.next_survey())
        previous_survey = Survey.objects.previous_survey()
        targeted_members_baseline = HouseholdMember.objects.filter(
            household_structure__household__plot__community__icontains=self.community,
            household_structure__survey=previous_survey,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            is_consented=True)
        targeted_members_internal_identifiers = [mem.internal_identifier for mem in targeted_members_baseline]
        targeted_members = HouseholdMember.objects.filter(household_structure__survey=current_annual_survey,
                                                          internal_identifier__in=targeted_members_internal_identifiers)
        # Create new threads
        thread1 = AnnualMember(1, "AnnualMember-1", 1, previous_survey, targeted_members_internal_identifiers,
                               self.data_dict, self.community, self.date_from, self.date_to, self.ra_username)
        thread2 = TargetedMember(2, "TargetedMember-2", 2, previous_survey, current_annual_survey, targeted_members,
                                 targeted_members_internal_identifiers, self.data_dict, self.community,
                                 self.date_from, self.date_to, self.ra_username)
        thread3 = NewMember(3, "NewMember-3", 3, previous_survey, current_annual_survey, self.data_dict,
                            self.community, self.date_from, self.date_to, self.ra_username)

        # Start new Threads
        thread1.start()
        thread2.start()
        thread3.start()

        # Add threads to thread list
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)

        # Wait for all threads to complete
        for t in threads:
            if t.is_alive():
                t.join()
        values = collections.OrderedDict(sorted(self.data_dict.items()))
        print "Exiting Main Thread"
        return values


class AnnualMember(threading.Thread):

    def __init__(self, thread_id, name, counter, previous_survey, targeted_members_internal_identifiers, data_dict,
                 community, date_from, date_to, ra_username):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.previous_survey = previous_survey
        self.targeted_members_internal_identifiers = targeted_members_internal_identifiers
        self.data_dict = data_dict
        self.community = community
        self.date_from = date_from
        self.date_to = date_to
        self.ra_username = ra_username

    def run(self):
        print "Starting " + self.name
        annual_member = HouseholdMember.objects.filter(
            household_structure__household__plot__community__icontains=self.community,
            household_structure__survey=self.previous_survey,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username)
        annual_internal_identifiers = [mem.internal_identifier for mem in annual_member]
        annual_members_reached = annual_member.exclude(Q(member_status=ABSENT) | Q(member_status=UNDECIDED)).count()
        self.data_dict['2. Annual BHS only members reached'] = annual_members_reached
        annual_new_hic_eligible = HicEnrollment.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__internal_identifier__in=annual_internal_identifiers,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username).exclude(subject_visit__household_member__internal_identifier__in=self.targeted_members_internal_identifiers).count()
        self.data_dict['91. Annual BHS members newly eligible for HIC'] = annual_new_hic_eligible
        annual_new_hic_enrolled = HicEnrollment.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__internal_identifier__in=annual_internal_identifiers,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            hic_permission='Yes').exclude(
                subject_visit__household_member__internal_identifier__in=self.targeted_members_internal_identifiers).count()
        self.data_dict['92. Annual BHS members newly eligible for HIC that enrolled'] = annual_new_hic_enrolled


class TargetedMember(threading.Thread):

    def __init__(self, thread_id, name, counter, previous_survey, current_annual_survey, targeted_members,
                 targeted_members_internal_identifiers, data_dict, community, date_from, date_to, ra_username):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.previous_survey = previous_survey
        self.current_annual_survey = current_annual_survey
        self.targeted_members = targeted_members
        self.targeted_members_internal_identifiers = targeted_members_internal_identifiers
        self.data_dict = data_dict
        self.community = community
        self.date_from = date_from
        self.date_to = date_to
        self.ra_username = ra_username

    def run(self):
        print "Starting " + self.name
#         targeted_members_internal_identifiers = [mem.internal_identifier for mem in self.targeted_members]
        targeted_members_unreached = self.targeted_members.exclude(member_status=ANNUAL).count()
        self.data_dict['3. Targeted BHS only members not reached'] = targeted_members_unreached
        targeted_members_relocated = self.targeted_members.filter(eligible_member=True).count()
        self.data_dict['4. Targeted BHS only members that relocated'] = 'N/A'
        targeted_members_deceased = self.targeted_members.filter(survival_status='dead').count()
        self.data_dict['5. Targeted BHS only members that are now deceased'] = targeted_members_deceased
        targeted_members_incarcerated = self.targeted_members.filter(eligible_member=True).count()
        self.data_dict['6. Targeted BHS only targeted_members are now incarcerated'] = 'N/A'
        targeted_eligible_retesting = 'N/A'
        self.data_dict['7. Targeted BHS members eligible for re-testing'] = targeted_eligible_retesting
        targeted_members_tested = HivResult.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__internal_identifier__in=self.targeted_members_internal_identifiers,
            subject_visit__household_member__household_structure__survey=self.current_annual_survey,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username).exclude(hiv_result='Declined').exclude(hiv_result='Not performed').count()
        self.data_dict['8. Targeted BHS members that tested'] = targeted_members_tested
        annual_declined_testing = HivResult.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__internal_identifier__in=self.targeted_members_internal_identifiers,
            subject_visit__household_member__household_structure__survey=self.current_annual_survey,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            hiv_result='Declined').count()
        self.data_dict['9. Targeted BHS members that declined testing'] = annual_declined_testing


class NewMember(threading.Thread):

    def __init__(self, thread_id, name, counter, previous_survey, current_annual_survey, data_dict, community,
                 date_from, date_to, ra_username):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.previous_survey = previous_survey
        self.current_annual_survey = current_annual_survey
        self.data_dict = data_dict
        self.community = community
        self.date_from = date_from
        self.date_to = date_to
        self.ra_username = ra_username

    def run(self):
        print "Starting " + self.name
        new_members_aggregate = HouseholdMember.objects.filter(
            household_structure__household__plot__community__icontains=self.community,
            household_structure__survey=self.current_annual_survey,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username).values('internal_identifier').annotate(dcount=Count('internal_identifier'))
        new_member_internal_indentifiers = []
        for mem in new_members_aggregate:
            if mem.get('dcount') == 1:
                new_member_internal_indentifiers.append(mem.get('internal_identifier'))
        new_members = HouseholdMember.objects.filter(internal_identifier__in=new_member_internal_indentifiers)
        self.data_dict['93. New members identified'] = new_members.count()
        new_consented = new_members.filter(is_consented=True).count()
        self.data_dict['94. New members consented'] = new_consented
        new_hic_eligible = HicEnrollment.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__internal_identifier__in=new_member_internal_indentifiers).count()
        self.data_dict['95. New members eligible for HIC'] = new_hic_eligible
        new_hic = HicEnrollment.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
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
        new_refused = SubjectRefusal.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            household_member__internal_identifier__in=new_member_internal_indentifiers).count()
        self.data_dict['993. New members that refused'] = new_refused
