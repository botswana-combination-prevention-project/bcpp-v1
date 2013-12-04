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

    #HouseholdMember
    community_members = HouseholdMember.objects.filter(household_structure__household__community=community1)
    members_refused = community_members.filter(member_status='REFUSED').count()

    first_time_testers = community_members.filter(subjectvisit__hivtestinghistory__has_tested='No')
    first_or_unknowns = first_time_testers.count()

    members_tested = community_members.exclude(subjectvisit__hivtested=None).count()

    page_context = {'communities': communities,
                    'plots': plots,
                    'households': households,
                    }
    return render(request, template, page_context)


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
        self.enumerated = self.enumerated_qs().count() or 1
        self.at_least_one_present = self.eligible_qs().distinct().count()
        self.all_refused = self.all_refused_qs().count()
        self.total_age_eligible = self.eligible_qs().count()
        self.average_age_eligible = float(self.total_age_eligible) / self.enumerated

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
