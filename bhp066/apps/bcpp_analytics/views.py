import collections
import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
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
    throwaway = datetime.datetime.strptime('20110101', '%Y%m%d')
    return datetime.datetime.strptime(date_string, date_format).date()


@login_required
def index(request):
    template = "bcpp_analytics/analytics_index.html"
    return render(request, template, {})


@login_required
@require_GET
def accrual(request):
    template = "bcpp_analytics/accrual_report.html"
    context = _process_accrual(request.GET, date_format=DEFAULT_DATE_FORMAT)
    context.update({'communities': communities})
    context.update({'action_url': 'analytics:accrual'})
    return render(request, template, context)


@login_required
@require_GET
def accrual_pdf(request, **kwargs):
    from .pdf.community_comparison_report import CommunityComparisonPDF
    from itertools import izip

    response = _pdf_response("community_accrual")
    result = _process_accrual(kwargs, date_format=STRFTIME_FORMAT)
    comm1_data = result['community1_data']
    comm2_data = result['community2_data']
    data = izip(comm1_data, comm2_data)
    pdf_data = {
        'data': data,
        'community1': comm1_data[0].community,
        'community2': comm2_data[0].community,
        'start_date': result['start_date'],
        'end_date': result['end_date'],
        'title': "Community Accrual",
        'report_variables': 'Accrual Variables',
    }
    CommunityComparisonPDF(pdf_data).build(response)
    return response


@login_required
@require_GET
def key_indicators(request):
    from .report_queries.indicators_report_query import IndicatorsReportQuery

    template = "bcpp_analytics/indicators_report.html"
    context = {'communities': communities}
    params = _prepare_params(request.GET, date_format=DEFAULT_DATE_FORMAT)
    context['community_pair'] = params['community_pair']
    start_date = params['start_date']
    end_date = params['end_date']
    report_data = []
    for community in params['community_pair']:
        indicator_data = IndicatorsReportQuery(community, start_date, end_date)
        report_data.append(indicator_data)
    context.update({'data': report_data})
    context['start_date'] = start_date.strftime(STRFTIME_FORMAT)
    context['end_date'] = end_date.strftime(STRFTIME_FORMAT)
    context.update({'action_url': 'analytics:indicators'})
    return render(request, template, context)


@login_required
@require_GET
def key_indicators_pdf(request, **kwargs):
    from .report_queries.indicators_report_query import IndicatorsReportQuery
    from .pdf.community_comparison_report import CommunityComparisonPDF

    response = _pdf_response("key_indicators_report")
    params = _prepare_params(kwargs, date_format=STRFTIME_FORMAT)
    community1 = params['community_pair'][0]
    community2 = params['community_pair'][1]
    data1 = IndicatorsReportQuery(community1, params["start_date"], params["end_date"])
    data2 = IndicatorsReportQuery(community2, params["start_date"], params["end_date"])
    data = [(data1, data2)]
    start_date = params['start_date']
    end_date = params['end_date']
    pdf_data = {
        'data': data,
        'community1': community1,
        'community2': community2,
        'start_date': start_date.strftime(STRFTIME_FORMAT),
        'end_date': end_date.strftime(STRFTIME_FORMAT),
        'title': 'Key Indicators',
        'report_variables': 'Indicators Variables',
    }
    CommunityComparisonPDF(pdf_data).build(response)
    return response


def _pdf_response(filename):
    from django.http import HttpResponse

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline;filename={0}.pdf'.format(filename)
    return response


def _process_accrual(params_dict, date_format):
    from .report_queries.household_visits_report_query import HouseholdVisitsReportQuery

    params = _prepare_params(params_dict, date_format)
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
        'report_data': report_data,
        'community1_data': report_data[0],
        'community2_data': report_data[1],
        'start_date': start_date.strftime(STRFTIME_FORMAT),
        'end_date': end_date.strftime(STRFTIME_FORMAT), }
    return context_data


def _prepare_params(params_dict, date_format):
    default_start = "Oct.  01, 2013" if date_format == STRFTIME_FORMAT else "01/10/2013"
    default_end = "Sep.  30, 2014" if date_format == STRFTIME_FORMAT else "30/09/2014"
    community1 = params_dict.get("com1", "Ranaka")
    community2 = params_dict.get("com2", "Digawana")
    start_date = date_from_s(params_dict.get("start") or default_start, date_format)
    end_date = date_from_s(params_dict.get("to") or default_end, date_format)
    return dict(community_pair=[community1, community2], start_date=start_date, end_date=end_date)


@login_required
def operational_report_view(request, **kwargs):
    values = {}
    utilities = OperatationalReportUtilities()
    ra_username = request.GET.get('ra', '')
    community = request.GET.get('community', '')
    previous_ra = ra_username
    previous_community = community
    if community.find('----') != -1:
        community = ''
    if ra_username.find('----') != -1:
        ra_username = ''
    date_from = utilities.date_format_utility(request.GET.get('date_from', ''), '1960/01/01')
    date_to = utilities.date_format_utility(request.GET.get('date_to', ''), '2099/12/31')

    plt = Plot.objects.all()
    reached = plt.filter(action='confirmed', community__icontains=community,
                         modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count()
    values['1. Plots reached'] = reached
    not_reached = plt.filter(action='unconfirmed', community__icontains=community,
                             modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count()
    values['2. Plots not reached'] = not_reached
    members = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=community,
                                             created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username)
    values['3. Total members'] = members.count()
    age_eligible = members.filter(eligible_member=True).count()
    values['4. Total age eligible members'] = age_eligible
    not_age_eligible = members.filter(eligible_member=False).count()
    values['5. Total members not age eligible'] = not_age_eligible
    age_eligible_research = members.filter(eligible_member=True, member_status_full='RESEARCH')
    research = age_eligible_research.count()
    values['6. Age eligible members that consented for RESEARCH'] = research
    age_eligible_htc = members.filter(eligible_member=True, member_status_partial='HTC')
    htc = age_eligible_htc.count()
    values['7. Age eligible members that consented for HTC ONLY'] = htc
    age_eligible_absent = members.filter(eligible_member=True, member_status_full='ABSENT')
    absent = age_eligible_absent.count()
    values['8. Age eligible members that where ABSENT'] = absent
    age_eligible_undecided = members.filter(eligible_member=True, member_status_full='UNDECIDED')
    undecided = age_eligible_undecided.count()
    values['9. Age eligible members that where UNDECIDED'] = undecided
    age_eligible_refused = members.filter(eligible_member=True, member_status_full='REFUSED')
    refused = age_eligible_refused.count()
    values['91. Age eligible members that REFUSED'] = refused
    how_many_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                               created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).count()
    values['92. Age eligible members that TESTED'] = how_many_tested
    values = collections.OrderedDict(sorted(values.items()))

    members_tobe_visited = []
    absentee_undecided = members.filter(eligible_member=True, visit_attempts__lte=3, household_structure__household__plot__community__icontains=community,
                                        created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).order_by('member_status_full')
    for mem in absentee_undecided:
        if mem.member_status_full == 'UNDECIDED':
            undecided_entries = SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=mem).order_by('next_appt_datetime')
            if undecided_entries:
                members_tobe_visited.append((str(mem), mem.member_status_full, mem.visit_attempts, str(undecided_entries[len(undecided_entries) - 1].next_appt_datetime)))
            else:
                members_tobe_visited.append((str(mem), mem.member_status_full, mem.visit_attempts, '-------'))
        elif mem.member_status_full == 'ABSENT':
            absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=mem).order_by('next_appt_datetime')
            if absentee_entries:
                members_tobe_visited.append((str(mem), mem.member_status_full, mem.visit_attempts, str(absentee_entries[len(absentee_entries) - 1].next_appt_datetime)))
            else:
                members_tobe_visited.append((str(mem), mem.member_status_full, mem.visit_attempts, '-------'))





#     my_entries = []
#     absentee_tobe_visited = []
#     absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member__household_structure__household__plot__community__icontains=community,
#                                                            created__gte=date_from, created__lte=date_to, user_modified__icontains=ra_username)
#    absentee_entries.count()
#     for absentee in age_eligible_absent:
#         my_entries = absentee_entries.filter(subject_absentee__registered_subject=absentee.registered_subject)
#         if my_entries and my_entries.count() < 3:
#             absentee_tobe_visited.append((str(absentee), my_entries.count(), str(my_entries.order_by('report_datetime')[len(my_entries) - 1].report_datetime)))
#         else:
#             absentee_tobe_visited.append((str(absentee), my_entries.count(), '--------'))

#     undecided_entries = SubjectUndecidedEntry.objects.filter(subject_undecided__household_member__household_structure__household__plot__community__icontains=community,
#                                                              created__gte=date_from, created__lte=date_to, user_modified__icontains=ra_username)
#     visits_per_undecided = []
#     for undecided in age_eligible_undecided:
#         my_entries = undecided_entries.filter(subject_undecided__registered_subject=undecided.registered_subject)
#         if my_entries and my_entries.count() < 3:
#             visits_per_undecided.append((str(undecided), my_entries.count(), str(my_entries.order_by('report_datetime')[len(my_entries) - 1].report_datetime)))
#         else:
#             visits_per_undecided.append((str(undecided), my_entries.count(), '--------'))

    #communities = [community[0].lower() for community in  COMMUNITIES]
    communities = []
    if (previous_community.find('----') == -1) and (not previous_community == ''):  # Passing filtered results
        #communities = [community[0].lower() for community in  COMMUNITIES]
        for community in  COMMUNITIES:
            if community[0].lower() != previous_community:
                communities.append(community[0])
        communities.insert(0, previous_community)
        communities.insert(1, '---------')
    else:
        communities = [community[0].lower() for community in  COMMUNITIES]
        communities.insert(0, '---------')

    ra_usernames = []
    if (previous_ra.find('----') == -1) and (not previous_ra == ''):
        for ra_name in [user.username for user in User.objects.filter(groups__name='field_research_assistant')]:
            if ra_name != previous_ra:
                ra_usernames.append(ra_name)
        ra_usernames.insert(0, previous_ra)
        ra_usernames.insert(1, '---------')
    else:
        ra_usernames = [user.username for user in User.objects.filter(groups__name='field_research_assistant')]
        ra_usernames.insert(0, '---------')

    return render_to_response(
        'bcpp_analytics/operational_report.html', {'values': values,
                                    'members_tobe_visited': members_tobe_visited,
                                    'communities': communities,
                                    'ra_usernames': ra_usernames},
        context_instance=RequestContext(request)
        )
