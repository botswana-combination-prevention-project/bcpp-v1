import collections
import datetime

from django.db.models import Max, Min
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models.loading import get_model

from apps.bcpp.choices import COMMUNITIES
from .report_queries.household_report_query import HouseholdReportQuery
from .report_queries.household_member_report_query import HouseholdMemberReportQuery
from .report_queries.plot_report_query import PlotReportQuery

from apps.bcpp_household.constants import NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION
from apps.bcpp_household.helpers import ReplacementHelper
from apps.bcpp_household.models import Plot
from apps.bcpp_household_member.constants import (ABSENT, BHS, HTC, REFUSED, UNDECIDED)
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import SubjectAbsenteeEntry, SubjectUndecidedEntry
from apps.bcpp_subject.models import HivResult
from apps.bcpp_survey.models import Survey
from django.shortcuts import render_to_response
from django.template import RequestContext
from edc.device.sync.models import Producer
from edc.core.bhp_birt_reports.classes import OperatationalReportUtilities


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
    
    date_from = utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
    date_to = utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')
    
    reached = 0
    not_reached = 0
    members_val = 0
    age_eligible = 0
    not_age_eligible =0
    research = 0
    htc = 0
    absent = 0
    undecided = 0
    refused = 0
    how_many_tested = 0
############################################################################################################################################
    if community == '':
        for item in COMMUNITIES:
            plt = Plot.objects.all()
            reached = reached + ( plt.filter(action='confirmed', community__icontains=community,
                                 modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count())
            values['1. Plots reached'] = reached
            not_reached = not_reached + (plt.filter(action='unconfirmed', community__icontains=community,
                                     modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count())
            values['2. Plots not reached'] = not_reached
            members = (HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=community,
                                                     created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username))
            members_val = members_val + (members.count())
            values['3. Total members'] = members_val
            
            age_eligible = age_eligible + (members.filter(eligible_member=True).count())
            values['4. Total age eligible members'] = age_eligible
            
            not_age_eligible = not_age_eligible + (members.filter(eligible_member=False).count())
            values['5. Total members not age eligible'] = not_age_eligible
            
            age_eligible_research = members.filter(eligible_member=True, member_status=BHS)
            research = research + (age_eligible_research.count())
            values['6. Age eligible members that consented for BHS'] = research
            
            age_eligible_htc = members.filter(eligible_member=True, member_status__in=HTC)
            htc = htc + (age_eligible_htc.count())
            values['7. Age eligible members that agreed to HTC (not through BHS)'] = htc
            
            age_eligible_absent = members.filter(eligible_member=True, member_status=ABSENT)
            absent = absent + (age_eligible_absent.count())
            values['8. Age eligible members that where ABSENT'] = absent
            
            age_eligible_undecided = members.filter(eligible_member=True, member_status=UNDECIDED)
            undecided = undecided + (age_eligible_undecided.count())
            values['9. Age eligible members that where UNDECIDED'] = undecided
            
            age_eligible_refused = members.filter(eligible_member=True, member_status=REFUSED)
            refused = refused + (age_eligible_refused.count())
            values['91. Age eligible members that REFUSED'] = refused
            
            how_many_tested =how_many_tested + (HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                                       created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).count())
            values['92. Age eligible members that TESTED'] = how_many_tested
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
###############################################################################
    elif ra_username == '':
        for user in User.objects.filter(groups__name='field_research_assistant'):
            plt = Plot.objects.all()
            reached = reached + ( plt.filter(action='confirmed', community__icontains=community,
                                 modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count())
            values['1. Plots reached'] = reached
            not_reached = not_reached + (plt.filter(action='unconfirmed', community__icontains=community,
                                     modified__gte=date_from, modified__lte=date_to, user_modified__icontains=ra_username).count())
            values['2. Plots not reached'] = not_reached
            members = (HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=community,
                                                     created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username))
            members_val = members_val + (members.count())
            
            values['3. Total members'] = members_val
            
            age_eligible = age_eligible + (members.filter(eligible_member=True).count())
            values['4. Total age eligible members'] = age_eligible
            
            not_age_eligible = not_age_eligible + (members.filter(eligible_member=False).count())
            values['5. Total members not age eligible'] = not_age_eligible
            
            age_eligible_research = members.filter(eligible_member=True, member_status=BHS)
            research = research + (age_eligible_research.count())
            values['6. Age eligible members that consented for BHS'] = research
            
            age_eligible_htc = members.filter(eligible_member=True, member_status__in=HTC)
            htc = htc + (age_eligible_htc.count())
            values['7. Age eligible members that agreed to HTC (not through BHS)'] = htc
            
            age_eligible_absent = members.filter(eligible_member=True, member_status=ABSENT)
            absent = absent + (age_eligible_absent.count())
            values['8. Age eligible members that where ABSENT'] = absent
            
            age_eligible_undecided = members.filter(eligible_member=True, member_status=UNDECIDED)
            undecided = undecided + (age_eligible_undecided.count())
            values['9. Age eligible members that where UNDECIDED'] = undecided
            
            age_eligible_refused = members.filter(eligible_member=True, member_status=REFUSED)
            refused = refused + (age_eligible_refused.count())
            values['91. Age eligible members that REFUSED'] = refused
            
            how_many_tested =how_many_tested + (HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                                       created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).count())
            values['92. Age eligible members that TESTED'] = how_many_tested
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
        
###################################################################################################################################
    else:
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
        age_eligible_research = members.filter(eligible_member=True, member_status=BHS)
        research = age_eligible_research.count()
        values['6. Age eligible members that consented for BHS'] = research
        age_eligible_htc = members.filter(eligible_member=True, member_status__in=HTC)
        htc = age_eligible_htc.count()
        values['7. Age eligible members that agreed to HTC (not through BHS)'] = htc
        age_eligible_absent = members.filter(eligible_member=True, member_status=ABSENT)
        absent = age_eligible_absent.count()
        values['8. Age eligible members that where ABSENT'] = absent
        age_eligible_undecided = members.filter(eligible_member=True, member_status=UNDECIDED)
        undecided = age_eligible_undecided.count()
        values['9. Age eligible members that where UNDECIDED'] = undecided
        age_eligible_refused = members.filter(eligible_member=True, member_status=REFUSED)
        refused = age_eligible_refused.count()
        values['91. Age eligible members that REFUSED'] = refused
        how_many_tested = HivResult.objects.filter(subject_visit__household_member__household_structure__household__plot__community__icontains=community,
                                                   created__gte=date_from, created__lte=date_to, user_created__icontains=ra_username).count()
        values['92. Age eligible members that TESTED'] = how_many_tested
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


@login_required
def replacement_report_view(request, **kwargs):

    replacement_values = {}
    accessment_forms_to_fill = 0
    household_refusal_forms_to_fill = 0
    replaceble_households = 0
    replaced_households = 0
    replaced_plots = 0
    replaceble_plots = 0
    plots = None
    replacement_helper = ReplacementHelper()
    first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
    survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
    household_structures = None
    producer_name = None
    households = None
    if request.POST.get('producer_name'):
        producer_name = request.POST.get('producer_name')
        p_ids = []
        plots = Plot.objects.filter(selected__in=[1, 2])
        for plot in plots:
            if producer_name.split('-')[0] == plot.producer_dispatched_to:
                p_ids.append(plot.id)
        plots = Plot.objects.filter(id__in=p_ids)
        households = get_model('bcpp_household', 'Household').objects.filter(plot__in=plots)
        household_structures = get_model('bcpp_household', 'HouseholdStructure').objects.filter(survey=survey, household__in=households)
    else:
        plots = Plot.objects.filter(selected__in=[1, 2])
        household_structures = get_model('bcpp_household', 'HouseholdStructure').objects.filter(survey=survey)
    producers = Producer.objects.all()
    producer_names = []
    for producer in producers:
        producer_names.append(producer.name)

    # Replaceble plots
    for plot in plots:
        replacement_helper.plot = plot
        if replacement_helper.replaceable_plot and not plot.replaced_by:
            replaceble_plots += 1
        if plot.replaced_by:
            replaced_plots += 1

    for household_structure in household_structures:
        household_status = None
        household_log = get_model('bcpp_household', 'HouseholdLog').objects.filter(household_structure=household_structure)
        # Replaceble households
        replacement_helper.household_structure = household_structure
        if replacement_helper.replaceable and not household_structure.household.replaced_by:
            replaceble_households += 1
        if household_structure.household.replaced_by:
            replaced_households += 1
        # Number of household assessment forms to fill
        try:
            report_datetime = get_model('bcpp_household', 'HouseholdLogEntry').objects.filter(household_log=household_log).aggregate(Max('report_datetime')).get('report_datetime__max')
            lastest_household_log_entry = get_model('bcpp_household', 'HouseholdLogEntry').objects.get(household_log__household_structure=household_structure, report_datetime=report_datetime)
            household_status = lastest_household_log_entry.household_status
        except get_model('bcpp_household', 'HouseholdLogEntry').DoesNotExist:
            household_status = None
        if household_structure.failed_enumeration_attempts == 3:
            if not get_model('bcpp_household', 'HouseholdAssessment').objects.filter(household_structure=household_structure) and household_status == NO_HOUSEHOLD_INFORMANT:
                accessment_forms_to_fill += 1
        elif not get_model('bcpp_household', 'HouseholdRefusal').objects.filter(household_structure=household_structure) and household_status == REFUSED_ENUMERATION:  # Refusals forms to fill
            household_refusal_forms_to_fill += 1

        replacement_values['1. Total replaced households'] = replaced_households
        replacement_values['2. Total replaced plots'] = replaced_plots
        replacement_values['3. Total number of replaceble households'] = replaceble_households
        replacement_values['4. Total household accessment pending'] = accessment_forms_to_fill
        replacement_values['5. Total Household refusals forms pending'] = household_refusal_forms_to_fill

        replacement_values = collections.OrderedDict(sorted(replacement_values.items()))

        return render_to_response(
        'bcpp_analytics/replacement_report.html', {
                            'replacement_values': replacement_values,
                            'producer_names': producer_names},
        context_instance=RequestContext(request)
        )
