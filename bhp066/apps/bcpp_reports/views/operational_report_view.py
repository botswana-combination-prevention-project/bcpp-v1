import collections

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from edc.core.bhp_birt_reports.classes import OperationalReportUtilities

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_household.constants import CONFIRMED, UNCONFIRMED
from bhp066.apps.bcpp_household_member.constants import ABSENT, UNDECIDED, REFUSED, HTC, BHS
from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.models import SubjectAbsenteeEntry, SubjectUndecidedEntry
from bhp066.apps.bcpp_subject.models import HivResult


@login_required
def operational_report_view(request, **kwargs):
    values = {}
    utilities = OperationalReportUtilities()
    community = request.GET.get('community', '')
    if community.find('----') != -1:
        community = ''
    date_from = utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
    date_to = utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')

    plt = Plot.objects.all()
    reached = plt.filter(action=CONFIRMED, community__icontains=community,
                         modified__gte=date_from, modified__lte=date_to).count()
    values['1. Plots reached'] = reached
    not_reached = plt.filter(action=UNCONFIRMED, community__icontains=community,
                             modified__gte=date_from, modified__lte=date_to).count()
    values['2. Plots not reached'] = not_reached
    members = HouseholdMember.objects.filter(household_structure__household__plot__community__icontains=community,
                                             created__gte=date_from, created__lte=date_to)
    values['3. Total members'] = members.count()
    age_eligible = members.filter(eligible_member=True).count()
    values['4. Total age eligible members'] = age_eligible
    not_age_eligible = members.filter(eligible_member=False).count()
    values['5. Total members not age eligible'] = not_age_eligible
    age_eligible_research = members.filter(eligible_member=True, member_status=BHS)
    research = age_eligible_research.count()
    values['6. Age eligible members that consented for RESEARCH'] = research
    age_eligible_htc = members.filter(eligible_member=True, member_status=HTC)
    htc = age_eligible_htc.count()
    values['7. Age eligible members that consented for HTC ONLY'] = htc
    age_eligible_absent = members.filter(Q(eligible_member=True) | Q(member_status=ABSENT))
    absent = age_eligible_absent.count()
    values['8. Age eligible members that where ABSENT'] = absent
    age_eligible_undecided = members.filter(eligible_member=True, member_status=UNDECIDED)
    undecided = age_eligible_undecided.count()
    values['9. Age eligible members that where UNDECIDED'] = undecided
    age_eligible_refused = members.filter(eligible_member=True, member_status=REFUSED)
    refused = age_eligible_refused.count()
    values['91. Age eligible members that REFUSED'] = refused
    how_many_tested = HivResult.objects.filter(
        subject_visit__household_member__household_structure__household__plot__community__icontains=community,
        created__gte=date_from, created__lte=date_to).count()
    values['92. Age eligible members that TESTED'] = how_many_tested
    values = collections.OrderedDict(sorted(values.items()))

    absentee_tobe_visited = []
    absentee_entries = SubjectAbsenteeEntry.objects.filter(
        subject_absentee__household_member__household_structure__household__plot__community__icontains=community,
        created__gte=date_from, created__lte=date_to)
    absentee_entries.count()
    for absentee in age_eligible_absent:
            if absentee_entries.filter(subject_absentee__registered_subject=absentee.registered_subject).count() < 3:
                    absentee_tobe_visited.append(
                        (str(absentee),
                         absentee_entries.filter(
                             subject_absentee__registered_subject=absentee.registered_subject).count()
                         )
                    )

    undecided_entries = SubjectUndecidedEntry.objects.filter(
        subject_undecided__household_member__household_structure__household__plot__community__icontains=community,
        created__gte=date_from, created__lte=date_to)
    visits_per_undecided = []
    for undecided in age_eligible_undecided:
            visits_per_undecided.append((str(undecided), undecided_entries.filter(
                subject_undecided__registered_subject=undecided.registered_subject).count()))

    communities = [com[0].lower() for com in COMMUNITIES]
    communities[0] = '---------'
    return render_to_response(
        # 'report_'+request.user.username+'_'+report_name+'.html', {},

        'operational_report.html', {'values': values,
                                    'absentee_tobe_visited': absentee_tobe_visited,
                                    'visits_per_undecided': visits_per_undecided,
                                    'communities': communities},
        context_instance=RequestContext(request)
    )
