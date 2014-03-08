from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.bcpp_dashboard.views import household_dashboard
from apps.bcpp_household_member.forms import ParticipationForm
from apps.bcpp_household_member.models import HouseholdMember, Loss
from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry, SubjectRefusal
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_FULL_PARTICIPATION, HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION


@login_required
def participation(request, **kwargs):
    """Updates the member status and redirects to the household dashboard."""
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('household_member')
            household_member = HouseholdMember.objects.get(pk=pk)
            if form.cleaned_data.get('status', None):
                update_member_status_full(request, household_member, form.cleaned_data)
            elif form.cleaned_data.get('status_partial', None):
                update_member_status_partial(request, household_member, form.cleaned_data)
            dashboard_type = form.cleaned_data.get('dashboard_type')
            dashboard_model = form.cleaned_data.get('dashboard_model')
            dashboard_id = form.cleaned_data.get('dashboard_id')
    else:
        # TODO: what happens if this gets passed? it fails!!
        dashboard_type = None
        dashboard_id = None
        dashboard_model = None

    return household_dashboard(request,
        dashboard_type=dashboard_type,
        dashboard_model=dashboard_model,
        dashboard_id=dashboard_id,
        # household_member=household_member,
        )

def update_member_status_partial(request, household_member, cleaned_data):
    """Updates the partial participation status.

    .. note:: if the member is consented, no changes are made."""
    status_partial = cleaned_data.get('status_partial', None)
    if not household_member.is_consented:
        # confirm you have a valid status or None
        if status_partial:
            if not status_partial in [item[0] for item in HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION]:
                raise TypeError('Unknown member status. Expected one on {0}, Got {1}.'.format([item[0] for item in HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION], status_partial))
        if SubjectRefusal.objects.filter(household_member=household_member).exists():
            #Potential BHS group that refused. Enforce a refusal form.
            refusal = SubjectRefusal.objects.get(household_member=household_member)
            if has_htc(status_partial) and refusal.accepted_htc:
                household_member.member_status_partial = status_partial
            elif has_htc(status_partial) and not refusal.accepted_htc:
                messages.add_message(request, messages.ERROR, 'Cannot make HTC as participant declined HTC in REFUSAL REPORT.')
            elif not has_htc(status_partial):
                household_member.member_status_partial = status_partial
            household_member.save()
        elif Loss.objects.filter(household_member=household_member).exists():
            #Group that failed BHS eligibility, they did not refuse and Loss form was created for them. Do not enforce refusal report.
            household_member.member_status_partial = status_partial
            household_member.save()
        elif household_member.age_in_years > 64:
            #Group that cannot take part in BHS, did not refuse, so do not enforce a refusal form.
            household_member.member_status_partial = status_partial
            household_member.save()
        else:
            messages.add_message(request, messages.ERROR, 'Please enter the refusal report before proceeding to partial participation.')
    return household_member.member_status_partial

def has_htc(status):
    if status.find('HTC') != -1:
        return True
    return False

def update_member_status_full(request, household_member, cleaned_data):
    """Updates the full participation status and possibly the eligibile_subject flag.

    .. note:: if the member is consented, no changes are made."""
    status = cleaned_data.get('status', None)
    if not household_member.is_consented:
        # confirm you have a valid status or None
        if status:
            if not status in [item[0] for item in HOUSEHOLD_MEMBER_FULL_PARTICIPATION]:
                raise TypeError('Unknown member status. Expected one on {0}, Got {1}.'.format([item[0] for item in HOUSEHOLD_MEMBER_FULL_PARTICIPATION], status))

        # changing from absent, clear subject_absentee if no entries for this member/survey if changing from absent to something else
        if household_member.member_status_full == 'ABSENT' and not status == 'ABSENT':
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=household_member):
                SubjectAbsentee.objects.filter(household_member=household_member).delete()

        # if changing to absent, set up a blank subject_absentee instance
        if not household_member.member_status_full == 'ABSENT' and status == 'ABSENT':
            if not SubjectAbsentee.objects.filter(household_member=household_member):
                SubjectAbsentee.objects.create(
                    registered_subject=household_member.registered_subject,
                    household_member=household_member,
                    report_datetime=datetime.today())

        if status == 'RESEARCH':
            if not household_member.member_status_full == status:
                # set status
                household_member.member_status_full = status
                household_member.save()
        # if anything other than RESEARCH and NOT_ELIGIBLE, clear eligibility flag and change
        elif status in [item[0] for item in HOUSEHOLD_MEMBER_FULL_PARTICIPATION if item[0] not in ['RESEARCH', 'NOT_ELIGIBLE']]:
            if not household_member.member_status_full == status:
                # clear eligibility flag then set status
                household_member.eligible_subject = False
                household_member.member_status_full = status
                household_member.save()
        elif status == 'NOT_ELIGIBLE':
            # do not allow to change to NOT ELIGIBLE if already has passed eligibility
            household_member.member_status_full = status
            household_member.save()
        else:
            pass
    return household_member.member_status_full
