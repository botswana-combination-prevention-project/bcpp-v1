from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

import datetime

from apps.bcpp_household.models.plot import Plot
from apps.bcpp_household.models.household import Household
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION as member_actions
from apps.bcpp_household_member.models.household_member import HouseholdMember
from apps.bcpp_subject.models.hiv_testing_history import HivTestingHistory
from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_subject.models.subject_consent import SubjectConsent


@login_required
def index(request):
    template = "bcpp_analytics/analytics_index.html"
    now = datetime.datetime.now()
    page_context = {'now': now, 'page_name': 'Reports Index'}
    return render(request, template, page_context)


@login_required
def accrual(request):
    template = "bcpp_analytics/accrual_report.html"
    communities = [item[0] for item in COMMUNITIES]
    community1 = request.GET.get("community1") or 'Ranaka'
    community2 = request.GET.get("community2") or 'Digawana'

    plots = (PlotReportQuery(community1), PlotReportQuery(community2))
    households = (HouseholdReportQuery(community1), HouseholdReportQuery(community2))
    members = (HouseholdMemberQuery(community1), HouseholdMemberQuery(community2))

    page_context = {'communities': communities,
                    'plots': plots,
                    'households': households,
                    'members': members,
                    }
    return render(request, template, page_context)


class HouseholdMemberQuery(object):
    def __init__(self, community):
        self.community = community
        self.community_members = HouseholdMember.objects.filter(household_structure__household__community=community)
        self.refused = self.refused_qs().count()
        self.first_time_testers = self.first_time_testers_qs().count()
        self.tested = self.tested_qs().count()
        self.age_eligible = self.age_eligible_qs().count()
        self.study_eligible = self.study_eligible_qs()
        self.unreached_after_2_visits = self.unreached_after_visits_qs(2).count()
        self.hiv_positives = self.hiv_positive_qs().count()

    def refused_qs(self):
        return self.community_members.filter(member_status='REFUSED')

    def first_time_testers_qs(self):
        return self.community_members.filter(subjectvisit__hivtestinghistory__has_tested='No')

    def age_eligible_qs(self):
        enrolled_ids = HouseholdReportQuery.enrolled_ids_qs(self.community)
        return self.community_members.filter(age_in_years__gte=16, household_structure__household_id__in=enrolled_ids)

    def tested_qs(self):
        return self.community_members.exclude(subjectvisit__hivtested=None)

    def study_eligible_qs(self):
        return SubjectConsent.objects.filter(household_member__household_structure__household__community=self.community).count()

    def reached_stats(self):
        return self._residents_demographics('REFUSED', 'UNDECIDED', 'RESEARCH')

    def enrolled_stats(self):
        return self._residents_demographics('RESEARCH')

    def _residents_demographics(self, *args):
        demographics = {}
        demo_query = self.community_members.filter(member_status__in=args)
        demographics['count'] = demo_query.count()
        demographics['males'] = demo_query.filter(gender='M').count()
        demographics['females'] = demo_query.filter(gender='F').count()
        age_ranges = [(16, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 79)]
        groups = {}
        for(a, b) in age_ranges:
            groups["{0}-{1}".format(a, b)] = demo_query.filter(age_in_years__range=(a, b)).count()
        demographics['age_groups'] = groups
        return demographics

    def unreached_after_visits_qs(self, no_of_visits):
        absentee_query = self.community_members.annotate(absentee_count=Count('subjectabsentee__subjectabsenteeentry'))
        return absentee_query.filter(absentee_count__gte=no_of_visits)

    def hiv_positive_qs(self):
        return self.community_members.filter(subjectvisit__hivresult__hiv_result='POS')


class PlotReportQuery(object):
    def __init__(self, community):
        self.community = community
        self.plots = Plot.objects.filter(community=community)
        self.targeted = self.targeted_qs().count()
        self.household_count = self.plot_stats().get('household_count')
        self.verified_residential = self.plot_stats().get('verified_count')

    def targeted_qs(self):
        return self.plots.exclude(selected=None)

    def confirmed_occupied_qs(self):
        return self.targeted_qs().filter(action='confirmed', status__istartswith='occupied')

    def plot_stats(self):
        return self.confirmed_occupied_qs().aggregate(household_count=Sum('household_count'), verified_count=Count('pk'))


class HouseholdReportQuery(object):

    def __init__(self, community):
        self.community = community
        self.targeted = self.targeted_qs().count()
        self.visited = self.visited_qs().count()
        self.enumerated = self.enumerated_qs().count()
        self.at_least_one_present = self.eligible_qs().distinct().count()
        self.all_refused = self.all_refused_qs().count()
        self.total_age_eligible = self.eligible_qs().count()
        self.average_age_eligible = float(self.total_age_eligible) / (self.enumerated or 1)

    def targeted_qs(self):
        return Household.objects.filter(plot__action='confirmed',
                                        plot__status__istartswith='occupied', community=self.community)

    def visited_qs(self):
        return self.targeted_qs().filter(householdstructure__householdlog__isnull=False)

    def enumerated_qs(self):
        return self.targeted_qs().filter(householdstructure__member_count__gte=1)

    def eligible_qs(self):
        return self.targeted_qs().filter(householdstructure__householdmember__eligible_member=True)

    def all_refused_qs(self):
        actions = [item[0] for item in member_actions if item[0] != 'REFUSED']
        return self.visited_qs().exclude(householdstructure__householdmember__member_status__in=actions)

    def age_elegible_qs(self):
        return self.enumerated_qs().filter(householdstructure__householdmember__eligible_member=True)

    @staticmethod
    def enrolled_qs(community):
        community_households = Household.objects.filter(community=community)
        return community_households.filter(householdstructure__householdmember__subjectconsent__isnull=False).distinct()

    @staticmethod
    def enrolled_ids_qs(community):
        ids = HouseholdReportQuery.enrolled_qs(community).values_list('id')
        return sum(ids, ())
