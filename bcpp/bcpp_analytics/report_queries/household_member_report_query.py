from collections import OrderedDict
from django.db.models import Count
from django.db.models import Q

from bhp066.apps.bcpp_household_member.models.household_member import HouseholdMember
from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent

from .household_report_query import HouseholdReportQuery
from .data_row import DataRow
from .report_query import TwoColumnReportQuery


class HouseholdMemberReportQuery(TwoColumnReportQuery):
    def post_init(self, **kwargs):
        self.community_members_qs = HouseholdMember.objects.filter(
            household_structure__household__community__iexact=self.community,
            created__gte=self.start_date, created__lte=self.end_date
        )

    def build(self):
        """builds up the report data"""
        self.absentees = self.absentee_stratified()
        self.refused = self.refused_qs().count()
        self.first_time_testers = self.first_time_testers_qs().count()
        self.tested = self.tested_qs().count()
        self.age_eligibles = self.age_eligible_qs().count()
        self.study_eligibles = self.study_eligible_qs().count()
        self.twice_unreached = self.unreached_after_visits_qs(2).count()
        self.hiv_positives = self.hiv_positive_qs().count()
        self.new_infections = self.new_infections_qs().count()
        self.already_infected = self.already_infected_qs().count()
        self.acknowledged_positives = self.self_reported_positive_qs().count()

    def display_title(self):
        return "Households Members/Residents"

    def data_to_display(self):
        self.build()
        data = []
        data.append(DataRow("Absentees stratified by visits", self.absentees))
        data.append(DataRow("Number Refused", self.refused))
        data.append(DataRow("First Time Testers", self.first_time_testers))
        data.append(DataRow('Eligible Members Tested', self.tested))
        data.append(DataRow('Age-Eligible in Enrolled Households', self.age_eligibles))
        data.append(DataRow('Study-Eligible in Enrolled Households', self.study_eligibles))
        data.append(DataRow('Demographics of Residents Reached', self.reached_stats()))
        data.append(DataRow('Demographics of Residents Enrolled', self.enrolled_stats()))
        data.append(DataRow('Unable to be reached after 2 visits', self.twice_unreached))
        data.append(DataRow('HIV persons in identified Households', self.hiv_positives))
        data.append(DataRow('New HIV Positives', self.new_infections))
        data.append(DataRow('Already Documented HIV positive', self.already_infected))
        data.append(DataRow('Self Reported as HIV positive', self.acknowledged_positives))
        return data

    def refused_qs(self):
        return self.community_members_qs.filter(refused=True)

    def absentee_stratified(self):
        absentee_strat = OrderedDict()
        absentee_strat['Absentees'] = self.absentee_qs().count()
        absentee_strat['Visit 1'] = self.unreached_after_visits_qs(1).count()
        absentee_strat['Visit 2'] = self.unreached_after_visits_qs(2).count()
        absentee_strat['Visit 3'] = self.unreached_after_visits_qs(3).count()
        return absentee_strat

    def first_time_testers_qs(self):
        return self.community_members_qs.filter(subjectvisit__hivtestinghistory__has_tested='No')

    def age_eligible_qs(self):
        enrolled_ids = HouseholdReportQuery.enrolled_ids_qs(self.community, self.start_date, self.end_date)
        return self.community_members_qs.filter(
            age_in_years__gte=16, household_structure__household_id__in=enrolled_ids)

    def tested_qs(self):
        return self.community_members_qs.filter(subjectvisit__hivtested__isnull=False)

    def study_eligible_qs(self):
        return SubjectConsent.objects.filter(
            household_member__household_structure__household__community__iexact=self.community,
            created__gte=self.start_date, created__lte=self.end_date)

    def reached_stats(self):
        return self._residents_demographics('REFUSED', 'UNDECIDED', 'RESEARCH')

    def absentee_qs(self):
        return self.community_members_qs.filter(absent=True)

    def enrolled_stats(self):
        return self._residents_demographics('RESEARCH')

    def _residents_demographics(self, *args):
        demographics = OrderedDict()
        # demo_query = self.community_members_qs.filter(member_status_full__in=args)
        demo_query = self.community_members_qs.filter(reported=True)
        demographics['Count'] = demo_query.count()
        demographics['Males'] = demo_query.filter(gender='M').count()
        demographics['Females'] = demo_query.filter(gender='F').count()
        age_ranges = [(16, 19), (20, 29), (30, 39), (40, 49), (50, 79)]
        groups = OrderedDict()
        groups['header'] = 'Age Groups'
        for(a, b) in age_ranges:
            groups["{0}-{1}".format(a, b)] = demo_query.filter(age_in_years__range=(a, b)).count()
        demographics['child_dict'] = groups
        return demographics

    def unreached_after_visits_qs(self, no_of_visits):
        absentee_count_query = self.absentee_qs().annotate(
            absentee_count=Count('subjectabsentee__subjectabsenteeentry'))
        return absentee_count_query.filter(absentee_count=no_of_visits)

    def self_reported_stats(self):
        stat = OrderedDict(count=self.self_reported_infected)
        stat['On ART'] = self.on_ART(self.self_reported_positive_qs()).count()
        stat['Not On ART'] = self.not_on_ART(self.self_reported_positive_qs()).count()
        return stat

    def documented_positive_stats(self):
        stat = OrderedDict(count=self.already_infected)
        stat['On ART'] = self.on_ART(self.already_infected_qs()).count()
        stat['Not On ART'] = self.not_on_ART(self.already_infected_qs()).count()
        return stat

    def hiv_positive_qs(self):
        return self.community_members_qs.filter(subjectvisit__hivresult__hiv_result='POS')

    def new_infections_qs(self):
        untested_Q = Q(subjectvisit__hivtestinghistory__has_tested='No')
        tested_Q = Q(subjectvisit__hivtestinghistory__verbal_hiv_result__in=['NEG', 'UNK', 'IND'])
        return self.hiv_positive_qs().filter(untested_Q | tested_Q)

    def already_infected_qs(self):
        review_Q = Q(subjectvisit__hivtestreview__recorded_hiv_result='POS')
        document_Q = Q(subjectvisit__hivresultdocumentation__result_recorded='POS')
        return self.hiv_positive_qs().filter(review_Q | document_Q)

    def self_reported_positive_qs(self):
        return self.hiv_positive_qs().filter(subjectvisit__hivtestinghistory__verbal_hiv_result='POS')

    def on_ART(self, hiv_positive_qs):
        return hiv_positive_qs.filter(subjectvisit__hivcareadherence__on_arv='Yes')

    def not_on_ART(self, hiv_positive_qs):
        return hiv_positive_qs.filter(subjectvisit__hivcareadherence__on_arv='No')
