from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

import datetime

from apps.bcpp_household.models.plot import Plot
from apps.bcpp_household.models.household import Household
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION as member_actions


@login_required
def index(request):
    template = "bcpp_reports/reports_index.html"
    now = datetime.datetime.now()
    page_context = {'now': now, 'page_name': 'Reports Index'}
    return render(request, template, page_context)


@login_required
def accrual(request):
    template = "bcpp_reports/accrual_report.html"
    community1 = 'ranaka'

    #community1
    plots = Plot.objects.filter(community=community1)
    targeted_plots = plots.exclude(selected=None)
    confirmed = targeted_plots.filter(action='confirmed')
    verified_residential = confirmed.filter(status__istartswith='occupied')

    targeted_count = targeted_plots.count()
    plot_stat = verified_residential.aggregate(Sum('household_count'), Count('pk'))

    #Households stats
    #targeted_households = Household.objects.filter(plot__action='confirmed', plot__status__istartswith='occupied',
    #                                               community=community1)
    #visited_households = targeted_households.filter(householdstructure__householdlog__isnull=False)

    #visited_households_count = visited_households.count()
    #enumerated_households = targeted_households.filter(householdstructure__member_count__gte=1)
    #enumerated_households_count = enumerated_households.count()

    #eligible_households = targeted_households.filter(householdstructure__householdmember__eligible_member=True).distint()
    #eligible_households_count = eligible_households.count()

    #actions = [item[0] for item in member_actions]
    #actions.remove('REFUSED')
    #all_refused_households = visited_households.exclude(householdstructure__householdmember__member_status__in=actions)
    #all_refused_count = all_refused_households.count()

    #total_age_eligible = enumerated_households.filter(householdstructure__householdmember__eligible_member=True)
    #total_age_eligible_count = total_age_eligible.count()

    #average_age_eligible = float(total_age_eligible_count)/enumerated_households_count

    #HouseholdMember

    household_report = HouseholdReportCommand('ranaka')
    page_context = {'targeted_count': targeted_count, 'plot_stats': plot_stat, 'household_data': household_report}
    return render(request, template, page_context)


class HouseholdReportCommand(object):

    def __init__(self, community):
        self.community = community
        self.targeted = self.targeted_qs().count()
        self.visited = self.visited_qs().count()
        self.enumerated = self.enumerated_qs().count()
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
