import collections
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

#from apps.bcpp_subject.models.hiv_testing_history import HivTestingHistory
from apps.bcpp.choices import COMMUNITIES
from .report_queries.household_report_query import HouseholdReportQuery
from .report_queries.household_member_report_query import HouseholdMemberReportQuery
from .report_queries.plot_report_query import PlotReportQuery

from django.db.models import Q
from edc.core.bhp_birt_reports.classes import OperatationalReportUtilities
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.bcpp_household.models import Plot
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import SubjectAbsenteeEntry, SubjectUndecidedEntry
from apps.bcpp_subject.models import HivResult


def date_from_s(date_string, date_format="%d/%m/%Y"):
    return datetime.datetime.strptime(date_string, date_format).date()


@login_required
def index(request):
    template = "bcpp_analytics/analytics_index.html"
    return render(request, template, {})


@login_required
@require_GET
def accrual(request):
    template = "bcpp_analytics/accrual_report.html"
    communities_list = [item[0] for item in COMMUNITIES]
    community1 = request.GET.get("community1", "Ranaka")
    community2 = request.GET.get("community2", "Digawana")
    start_date = date_from_s(request.GET.get("start_date", "01/10/2013"))
    end_date = date_from_s(request.GET.get("end_date", "30/09/2014"))

    plots = (PlotReportQuery(community1, start_date, end_date), PlotReportQuery(community2, start_date, end_date))
    households = (HouseholdReportQuery(community1, start_date, end_date), HouseholdReportQuery(community2, start_date, end_date))
    members = (HouseholdMemberReportQuery(community1, start_date, end_date), HouseholdMemberReportQuery(community2, start_date, end_date))
    report_data = [plots, households, members]
    community1_data = [item[0] for item in report_data]
    community2_data = [item[1] for item in report_data]

    page_context = {'communities_list': communities_list,
                    'community1_data': community1_data,
                    'community2_data': community2_data,
                    'start_date': start_date.strftime("%b.  %d, %Y"),
                    'end_date': end_date.strftime("%b.  %d, %Y"),
                    }
    return render(request, template, page_context)


@login_required
def operational_report_view(request, **kwargs):
    values = {}
    utilities = OperatationalReportUtilities()
    community = request.GET.get('community', '')
    previous_community = community
    if community.find('----') != -1:
        community = ''
    date_from = utilities.date_format_utility(request.GET.get('date_from', ''), '1960/01/01')
    date_to = utilities.date_format_utility(request.GET.get('date_to', ''), '2099/12/31')

    plt = Plot.objects.all()
    reached = plt.filter(action='confirmed', community__icontains=community,
                         modified__gte=date_from, modified__lte=date_to).count()
    values['1. Plots reached'] = reached
    not_reached = plt.filter(action='unconfirmed', community__icontains=community,
                             modified__gte=date_from, modified__lte=date_to).count()
    values['2. Plots not reached'] = not_reached
    members = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=community,
                                             created__gte=date_from, created__lte=date_to)
    values['3. Total members'] = members.count()
    age_eligible = members.filter(eligible_member=True).count()
    values['4. Total age eligible members'] = age_eligible
    not_age_eligible = members.filter(eligible_member=False).count()
    values['5. Total members not age eligible'] = not_age_eligible
    age_eligible_research = members.filter(eligible_member=True, member_status='RESEARCH')
    research = age_eligible_research.count()
    values['6. Age eligible members that consented for RESEARCH'] = research
    age_eligible_htc = members.filter(eligible_member=True, member_status='HTC')
    htc = age_eligible_htc.count()
    values['7. Age eligible members that consented for HTC ONLY'] = htc
    age_eligible_absent = members.filter(Q(eligible_member=True) | Q(member_status='ABSENT'))
    absent = age_eligible_absent.count()
    values['8. Age eligible members that where ABSENT'] = absent
    age_eligible_undecided = members.filter(eligible_member=True, member_status='UNDECIDED')
    undecided = age_eligible_undecided.count()
    values['9. Age eligible members that where UNDECIDED'] = undecided
    age_eligible_refused = members.filter(eligible_member=True, member_status='REFUSED')
    refused = age_eligible_refused.count()
    values['91. Age eligible members that REFUSED'] = refused
    how_many_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                               created__gte=date_from, created__lte=date_to).count()
    values['92. Age eligible members that TESTED'] = how_many_tested
    values = collections.OrderedDict(sorted(values.items()))

    absentee_tobe_visited = []
    absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member__household_structure__household__plot__community__icontains=community,
                                                           created__gte=date_from, created__lte=date_to)
    absentee_entries.count()
    for absentee in age_eligible_absent:
            if absentee_entries.filter(subject_absentee__registered_subject=absentee.registered_subject).count() < 3:
                    absentee_tobe_visited.append((str(absentee), absentee_entries.filter(subject_absentee__registered_subject=absentee.registered_subject).count()))

    undecided_entries = SubjectUndecidedEntry.objects.filter(subject_undecided__household_member__household_structure__household__plot__community__icontains=community,
                                                             created__gte=date_from, created__lte=date_to)
    visits_per_undecided = []
    for undecided in age_eligible_undecided:
            visits_per_undecided.append((str(undecided), undecided_entries.filter(subject_undecided__registered_subject=undecided.registered_subject).count()))

    #communities = [community[0].lower() for community in  COMMUNITIES]
    communities = []
    if previous_community.find('----') == -1 and not previous_community == '':#Passing filtered results
        #communities = [community[0].lower() for community in  COMMUNITIES]
        for community in  COMMUNITIES:
            if community[0].lower() != previous_community:
                communities.append(community[0])
        communities.insert(0, previous_community)
        communities.insert(1, '---------')
    else:
        communities = [community[0].lower() for community in  COMMUNITIES]
        communities.insert(0, '---------')
    return render_to_response(
        # 'report_'+request.user.username+'_'+report_name+'.html', {},

        'bcpp_analytics/operational_report.html', {'values': values,
                                    'absentee_tobe_visited': absentee_tobe_visited,
                                    'visits_per_undecided': visits_per_undecided,
                                    'communities': communities},
        context_instance=RequestContext(request)
        )
