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
            household_member = HouseholdMember.objects.get(pk=form.cleaned_data.get('household_member'))
            if not household_member.is_consented:
                if form.cleaned_data.get('status'):  # status_full
                    #update_member_status_full(household_member, form.cleaned_data.get('status'))
                    household_member.member_status_full = form.cleaned_data.get('status')
                    household_member.save()
                elif form.cleaned_data.get('status_partial', None):
                    error_messages = update_member_status_partial(household_member, form.cleaned_data.get('status_partial'))
                    for msg in error_messages:
                        messages.add_message(request, messages.ERROR, msg)
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
        )


def update_member_status_partial(household_member, selected_status):
    """Updates the partial participation status.

    .. note:: if the member is consented, no changes are made."""
    error_messages = []
    member_status_partial = household_member.member_status_partial
    if is_valid_status_partial(selected_status):
        if SubjectRefusal.objects.filter(household_member=household_member).exists():
            # Potential BHS group that refused. Enforce a refusal form.
            refusal = SubjectRefusal.objects.get(household_member=household_member)
            if has_htc(selected_status) and refusal.accepted_htc:
                member_status_partial = selected_status
            elif has_htc(selected_status) and not refusal.accepted_htc:
                error_messages.append('Cannot make HTC as participant declined HTC in REFUSAL REPORT.')
            elif not has_htc(selected_status):
                member_status_partial = selected_status
        elif Loss.objects.filter(household_member=household_member).exists():
            # Group that failed BHS eligibility, they did not refuse and Loss form was created for them. Do not enforce refusal report.
            member_status_partial = selected_status
        elif household_member.age_in_years > 64:
            # Group that cannot take part in BHS, did not refuse, so do not enforce a refusal form.
            member_status_partial = selected_status
        else:
            error_messages.append('Please enter the refusal report before proceeding to partial participation.')
        if household_member.member_status_partial != member_status_partial:
            household_member.member_status_partial = member_status_partial
            household_member.save()
    return error_messages


def update_member_status_full(household_member, selected_status):
    """Updates the full participation status and possibly the eligibile_subject flag.

    .. note:: if the member is consented, no changes are made."""
    member_status_full = household_member.member_status_full
    eligible_subject = household_member.eligible_subject
    if is_valid_status_full(selected_status):
        # changing from absent, clear subject_absentee if no entries for this member/survey if changing from absent to something else
        if household_member.member_status_full == 'ABSENT' and not selected_status == 'ABSENT':
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=household_member):
                SubjectAbsentee.objects.filter(household_member=household_member).delete()
        # if changing to absent, set up a blank subject_absentee instance
        if not household_member.member_status_full == 'ABSENT' and selected_status == 'ABSENT':
            if not SubjectAbsentee.objects.filter(household_member=household_member):
                SubjectAbsentee.objects.create(
                    registered_subject=household_member.registered_subject,
                    household_member=household_member,
                    report_datetime=datetime.today())
        if selected_status == 'RESEARCH':
            member_status_full = selected_status
        elif selected_status == 'NOT_ELIGIBLE':
            # do not allow to change to NOT ELIGIBLE if already has passed eligibility
            member_status_full = selected_status
        else:
            # if anything other than RESEARCH and NOT_ELIGIBLE, clear eligibility flag and change
            # clear eligibility flag then set status
            eligible_subject = False  # Why?
            member_status_full = selected_status
        if household_member.member_status_full != member_status_full:
            household_member.member_status_full = member_status_full
            household_member.eligible_subject = eligible_subject
            household_member.save()
    return member_status_full


def is_valid_status_partial(status_partial):
    if not status_partial in [item[0] for item in HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION]:
        raise TypeError('Unknown member status. Expected one on {0}, Got {1}.'.format([item[0] for item in HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION], status_partial))
    return True


def is_valid_status_full(status_full):
    if not status_full in [item[0] for item in HOUSEHOLD_MEMBER_FULL_PARTICIPATION]:
            raise TypeError('Unknown member status. Expected one on {0}, Got {1}.'.format([item[0] for item in HOUSEHOLD_MEMBER_FULL_PARTICIPATION], status_full))
    return True


def has_htc(status):
    if status.find('HTC') != -1:
        return True
    return False
