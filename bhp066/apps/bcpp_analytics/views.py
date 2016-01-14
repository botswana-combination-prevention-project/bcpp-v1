import collections
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Min
from django.db.models.loading import get_model
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_GET

from edc.core.bhp_birt_reports.classes import OperationalReportUtilities
from edc.device.sync.models import Producer

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_household.constants import (
    NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION,
    CONFIRMED, UNCONFIRMED)
from bhp066.apps.bcpp_subject.constants import DECLINED, NOT_PERFORMED
from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_household_member.constants import (ABSENT, BHS, HTC, UNDECIDED)
from bhp066.apps.bcpp_household_member.models import HouseholdMember, SubjectRefusal
from bhp066.apps.bcpp_household_member.models import SubjectAbsenteeEntry, SubjectUndecidedEntry
from bhp066.apps.bcpp_subject.models import HivResult, HicEnrollment
from bhp066.apps.bcpp_survey.models import Survey

from .classes import (OperationalPlots, OperationalHousehold, OperationalMember,
                      OperationalSpecimen, OperationalAnnual, OperationalRbd, OperationalVisits,
                      OperationalConsents)
from .report_queries.household_member_report_query import HouseholdMemberReportQuery
from .report_queries.household_report_query import HouseholdReportQuery
from .report_queries.plot_report_query import PlotReportQuery


DEFAULT_DATE_FORMAT = "%d-%m-%Y"
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
    default_start = "Oct.  01, 2013" if date_format == STRFTIME_FORMAT else "01-10-2013"
    default_end = "Sep.  30, 2014" if date_format == STRFTIME_FORMAT else "30-09-2014"
    community1 = params_dict.get("com1", "Ranaka")
    community2 = params_dict.get("com2", "Digawana")
    start_date = date_from_s(params_dict.get("start") or default_start, date_format)
    end_date = date_from_s(params_dict.get("to") or default_end, date_format)
    return dict(community_pair=[community1, community2], start_date=start_date, end_date=end_date)


@login_required
def operational_report_plots_view(request, **kwargs):
    operational_plots = OperationalPlots(request)
    return render_to_response(
        'bcpp_analytics/operational_report_plot.html', {'values': operational_plots.build_report(),
                                                        'communities': operational_plots.return_communities(),
                                                        'ra_usernames': operational_plots.return_ra_usernames()},
        context_instance=RequestContext(request))


@login_required
def operational_report_household_view(request, **kwargs):
    operational_household = OperationalHousehold(request)
    return render_to_response(
        'bcpp_analytics/operational_report_household.html', {'values': operational_household.build_report(),
                                                        'communities': operational_household.return_communities(),
                                                        'ra_usernames': operational_household.return_ra_usernames(),},
        context_instance=RequestContext(request))


@login_required
def operational_report_member_view(request, **kwargs):
    operational_member = OperationalMember(request)
    return render_to_response(
        'bcpp_analytics/operational_report_member.html', {'values': operational_member.build_report(),
                                                        'communities': operational_member.return_communities(),
                                                        'ra_usernames': operational_member.return_ra_usernames(),
                                                        'surveys': operational_member.return_surveys()},
        context_instance=RequestContext(request))


@login_required
def operational_report_specimen_view(request, **kwargs):
    operational_specimen = OperationalSpecimen(request)
    return render_to_response(
        'bcpp_analytics/operational_report_specimen.html', {'values': operational_specimen.build_report(),
                                                        'communities': operational_specimen.return_communities(),
                                                        'ra_usernames': operational_specimen.return_ra_usernames(),
                                                        'surveys': operational_specimen.return_surveys()},
        context_instance=RequestContext(request))


@login_required
def operational_report_annual_view(request, **kwargs):
    operational_annual = OperationalAnnual(request)
    return render_to_response(
        'bcpp_analytics/operational_report_annual.html', {'values': operational_annual.build_report(),
                                                        'communities': operational_annual.return_communities(),
                                                        'ra_usernames': operational_annual.return_ra_usernames()},
        context_instance=RequestContext(request))


@login_required
def operational_report_rbd_view(request, **kwargs):
    operational_rbd = OperationalRbd(request)
    return render_to_response(
        'bcpp_analytics/operational_report_rbd.html', {
            'values': operational_rbd.build_report(),
            'communities': operational_rbd.return_communities(),
            'ra_usernames': operational_rbd.return_ra_usernames()},
        context_instance=RequestContext(request))


@login_required
def operational_report_consents_view(request, **kwargs):
    operational_consents = OperationalConsents(request)
    return render_to_response(
        'bcpp_analytics/operational_report_consents.html', {
            'values': operational_consents.build_report(),
            'communities': operational_consents.return_communities(),
            'ra_usernames': operational_consents.return_ra_usernames()},
        context_instance=RequestContext(request))


@login_required
def operational_report_visits_view(request, **kwargs):
    operational_visits = OperationalVisits(request)
    return render_to_response(
        'bcpp_analytics/operational_report_visits.html', {
            'values': operational_visits.build_report(),
            'communities': operational_visits.return_communities(),
            'ra_usernames': operational_visits.return_ra_usernames()},
        context_instance=RequestContext(request))


@login_required
def operational_report_view(request, **kwargs):
    values = {}
    utilities = OperationalReportUtilities()
    ra_username = request.GET.get('ra', '')
    community = request.GET.get('community', '')
    previous_ra = ra_username
    previous_community = community

    if community.find('----') != -1:
        community = ''

    if ra_username.find('----') != -1:
        ra_username = ''

    date_from = utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
    date_to = utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')

    date_to += datetime.timedelta(days=1)
    plt = Plot.objects.all()
    reached = (plt.filter(action=CONFIRMED, community__icontains=community,
                                    modified__gte=date_from, modified__lte=date_to,
                                    user_modified__icontains=ra_username).count())
    values['1. Plots reached'] = reached
    not_reached = (plt.filter(action=UNCONFIRMED, community__icontains=community,
                                            modified__gte=date_from, modified__lte=date_to,
                                            user_modified__icontains=ra_username).count())
    values['2. Plots not reached'] = not_reached
    members = (HouseholdMember.objects.filter(
        household_structure__household__plot__community__icontains=community,
        created__gte=date_from, created__lte=date_to,
        user_created__icontains=ra_username))
    members_val = (members.count())

    values['3. Total members'] = members_val

    age_eligible = (members.filter(eligible_member=True).count())
    values['4. Total age eligible members'] = age_eligible

    not_age_eligible = (members.filter(eligible_member=False).count())
    values['5. Total members not age eligible'] = not_age_eligible

    age_eligible_research = members.filter(eligible_member=True, member_status=BHS)
    research = (age_eligible_research.count())
    values['6. Age eligible members that consented for BHS'] = research

    age_eligible_htc = members.filter(member_status=HTC)
    htc = (age_eligible_htc.count())
    values['7. Age eligible members that agreed to HTC (not through BHS)'] = htc

    age_eligible_absent = members.filter(eligible_member=True, member_status=ABSENT)
    absent = (age_eligible_absent.count())
    values['8. Age eligible members that where ABSENT'] = absent

    age_eligible_undecided = members.filter(eligible_member=True, member_status=UNDECIDED)
    undecided = (age_eligible_undecided.count())
    values['9. Age eligible members that where UNDECIDED'] = undecided

    age_eligible_refused = SubjectRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=community)
    refused = age_eligible_refused.count()
    values['91. Age eligible members that REFUSED'] = refused
    how_many_tested = (HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                         created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).exclude(hiv_result__in=[DECLINED, NOT_PERFORMED]).count())
    values['92. Age eligible members that TESTED'] = how_many_tested
    how_many_hic = (HicEnrollment.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                         created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username, hic_permission='Yes').count())
    values['93. Age eligible members enrolled in to HIC'] = how_many_hic
    values = collections.OrderedDict(sorted(values.items()))
    members_tobe_visited = []
    absentee_undecided = members.filter(eligible_member=True, visit_attempts__lte=3, household_structure__household__plot__community__icontains=community,
                                        created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).order_by('member_status')
    for mem in absentee_undecided:
        if mem.member_status == UNDECIDED:
            undecided_entries = SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=mem).order_by('next_appt_datetime')
            if undecided_entries and mem.visit_attempts < 3:
                members_tobe_visited.append((str(mem), mem.member_status, mem.visit_attempts, str(undecided_entries[len(undecided_entries) - 1].next_appt_datetime)))
            elif mem.visit_attempts < 3:
                members_tobe_visited.append((str(mem), mem.member_status, mem.visit_attempts, '-------'))
        elif mem.member_status == ABSENT:
            absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=mem).order_by('next_appt_datetime')
            if absentee_entries and mem.visit_attempts < 3:
                members_tobe_visited.append((str(mem), mem.member_status, mem.visit_attempts, str(absentee_entries[len(absentee_entries) - 1].next_appt_datetime)))
            elif mem.visit_attempts < 3:
                members_tobe_visited.append((str(mem), mem.member_status, mem.visit_attempts, '-------'))
    communities = []
    if (previous_community.find('----') == -1) and (not previous_community == ''):  # Passing filtered results
        # communities = [community[0].lower() for community in  COMMUNITIES]
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
        context_instance=RequestContext(request))


@login_required
def replacement_report_view(request, **kwargs):

    replacement_values = {}
    accessment_forms_to_fill = 0
    household_refusal_forms_to_fill = 0
    replaceable_households = 0
    replaced_households = 0
    replaced_plots = 0
    replaceable_plots = 0
    plots = None
    household_structures = None
    producer_name = None
    households = None
    HouseholdLogEntry = get_model('bcpp_household', 'HouseholdLogEntry')
    Household = get_model('bcpp_household', 'Household')
    HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
    HouseholdLog = get_model('bcpp_household', 'HouseholdLog')
    HouseholdAssessment = get_model('bcpp_household', 'HouseholdAssessment')
    HouseholdRefusal = get_model('bcpp_household', 'HouseholdRefusal')
    first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
    survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
    if request.POST.get('producer_name'):
        producer_name = request.POST.get('producer_name')
        p_ids = []
        plots = (plot for plot in Plot.objects.filter(selected__in=[1, 2]) if plot.dispatched_to == producer_name)
        for plot in plots:
            if producer_name == plot.dispatched_to:
                p_ids.append(plot.id)
        plots = Plot.objects.filter(id__in=p_ids)
        households = Household.objects.filter(plot__in=plots)
        household_structures = HouseholdStructure.objects.filter(survey=survey, household__in=households)
    else:
        plots = Plot.objects.filter(selected__in=[1, 2])
        household_structures = HouseholdStructure.objects.filter(survey=survey)
    producers = Producer.objects.all()
    producer_names = []
    for producer in producers:
        producer_names.append(producer.name)

    # replaceable plots
    for plot in plots:
        if plot.replaceable:
            replaceable_plots += 1
        if plot.replaced_by:
            replaced_plots += 1
    for household_structure in household_structures:
        household_status = None
        household_log = HouseholdLog.objects.filter(household_structure=household_structure)
        # replaceable households
        if household_structure.household.replaceable:
            replaceable_households += 1
        if household_structure.household.replaced_by:
            replaced_households += 1
        # Number of household assessment forms to fill
        try:
            report_datetime = HouseholdLogEntry.objects.filter(household_log=household_log).aggregate(Max('report_datetime')).get('report_datetime__max')
            lastest_household_log_entry = HouseholdLogEntry.objects.get(household_log__household_structure=household_structure, report_datetime=report_datetime)
            household_status = lastest_household_log_entry.household_status
        except HouseholdLogEntry.DoesNotExist:
            household_status = None
        if household_structure.failed_enumeration_attempts == 3:
            if not HouseholdAssessment.objects.filter(household_structure=household_structure) and household_status == NO_HOUSEHOLD_INFORMANT:
                accessment_forms_to_fill += 1
        elif not HouseholdRefusal.objects.filter(household_structure=household_structure) and household_status == REFUSED_ENUMERATION:  # Refusals forms to fill
            household_refusal_forms_to_fill += 1

    replacement_values['1. Total replaced households'] = replaced_households
    replacement_values['2. Total replaced plots'] = 23
    replacement_values['3. Total number of replaceable households'] = replaceable_households
    replacement_values['4. Total household assessment pending'] = accessment_forms_to_fill
    replacement_values['5. Total Household refusals forms pending'] = household_refusal_forms_to_fill

    replacement_values = collections.OrderedDict(sorted(replacement_values.items()))

    return render_to_response(
        'bcpp_analytics/replacement_report.html', {
            'replacement_values': replacement_values,
            'producer_names': producer_names},
        context_instance=RequestContext(request)
    )
