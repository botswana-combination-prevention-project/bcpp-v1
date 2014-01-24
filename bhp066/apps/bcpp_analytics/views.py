import collections
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

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


DEFAULT_DATE_FORMAT = "%d/%m/%Y"
STRFTIME_FORMAT = "%b.  %d, %Y"

communities = [item[0] for item in COMMUNITIES]


def date_from_s(date_string, date_format=DEFAULT_DATE_FORMAT):
    # This is a throwaway variable to deal with a python _strptime import bug
    throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
    return datetime.datetime.strptime(date_string, date_format).date()


@login_required
def index(request):
    template = "bcpp_analytics/analytics_index.html"
    return render(request, template, {})


@login_required
@require_GET
def accrual(request):
    template = "bcpp_analytics/accrual_report.html"
    context = _process_accrual(request, date_format=DEFAULT_DATE_FORMAT)
    context.update({'communities': communities})
    return render(request, template,  context)


@login_required
@require_GET
def accrual_pdf(request, **kwargs):
    from .pdf.accrual_report import AccrualPDFReport

    pdf_data = _process_accrual(request, date_format=STRFTIME_FORMAT)
    return AccrualPDFReport(pdf_data).display(request)


@login_required
@require_GET
def key_indicators(request):
    from .report_queries.indicators_report_query import IndicatorsReportQuery

    template = "bcpp_analytics/indicators_report.html"
    context = {'communities': communities}
    params = _prepare_params(request, date_format=DEFAULT_DATE_FORMAT)
    context.update(params)
    report_data = []
    for community in params['community_pair']:
        indicator_data = IndicatorsReportQuery(community, params["start_date"], params["end_date"])
        report_data.append(indicator_data)
    context.update({'data': report_data})
    return render(request, template, context)


def _process_accrual(req, date_format):
    from .report_queries.household_visits_report_query import HouseholdVisitsReportQuery

    params = _prepare_params(req, date_format)
    start_date = params['start_date']
    end_date = params['end_date']
    report_data = []
    for community in params['community_pair']:
        community_data = []
        community_data.append(PlotReportQuery(community, start_date, end_date))
        community_data.append(HouseholdReportQuery(community, start_date, end_date))
        community_data.append(HouseholdMemberReportQuery(community, start_date, end_date))
        community_data.append(HouseholdVisitsReportQuery(community, start_date, end_date))
        report_data.append(community_data)
    context_data = {
        'community1_data': report_data[0],
        'community2_data': report_data[1],
        'start_date': start_date.strftime(STRFTIME_FORMAT),
        'end_date': end_date.strftime(STRFTIME_FORMAT), }
    return context_data


def _prepare_params(req, date_format):
    default_start = "Oct.  01, 2013" if date_format == STRFTIME_FORMAT else "01/10/2013"
    default_end = "Sep.  30, 2014" if date_format == STRFTIME_FORMAT else "30/09/2014"
    community1 = req.GET.get("com1", "Ranaka")
    community2 = req.GET.get("com2", "Digawana")
    start_date = date_from_s(req.GET.get("start") or default_start, date_format)
    end_date = date_from_s(req.GET.get("to") or default_end, date_format)
    return dict(community_pair=[community1, community2], start_date=start_date, end_date=end_date)


@login_required
def operational_report_view(request, **kwargs):
    values = {}
    utilities = OperatationalReportUtilities()
    community = request.GET.get('community', '')
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

    communities = [community[0].lower() for community in  COMMUNITIES]
    communities[0] = '---------'
    return render_to_response(
        # 'report_'+request.user.username+'_'+report_name+'.html', {},

        'bcpp_analytics/operational_report.html', {'values': values,
                                    'absentee_tobe_visited': absentee_tobe_visited,
                                    'visits_per_undecided': visits_per_undecided,
                                    'communities': communities},
        context_instance=RequestContext(request)
        )
