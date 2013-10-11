from datetime import datetime
from django.contrib.auth.decorators import login_required
from apps.bcpp_dashboard.views import household_dashboard
from apps.bcpp_household_member.forms import ParticipationForm
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry
from apps.bcpp_household.choices import HOUSEHOLD_MEMBER_ACTION


@login_required
def participation(request, **kwargs):
    """Updates the member status and redirects to the household dashboard."""
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('household_member')
            household_member = HouseholdMember.objects.get(pk=pk)
            update_member_status(household_member, form.cleaned_data)
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


def update_member_status(household_member, cleaned_data):
    """Updates the status and possibly the eligibile_subject flag.

    .. note:: if the member is consented, no changes are made."""
    status = cleaned_data.get('status', None)
    if not household_member.is_consented:
        # confirm you have a valid status or None
        if status:
            if not status in [item[0] for item in HOUSEHOLD_MEMBER_ACTION]:
                raise TypeError('Unknown member status. Expected one on {0}, Got {1}.'.format([item[0] for item in HOUSEHOLD_MEMBER_ACTION], status))

        # changing from absent, clear subject_absentee if no entries for this member/survey if changing from absent to something else
        if household_member.member_status == 'ABSENT' and not status == 'ABSENT':
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=household_member):
                SubjectAbsentee.objects.filter(household_member=household_member).delete()

        # if changing to absent, set up a blank subject_absentee instance
        if not household_member.member_status == 'ABSENT' and status == 'ABSENT':
            if not SubjectAbsentee.objects.filter(household_member=household_member):
                SubjectAbsentee.objects.create(
                    registered_subject=household_member.registered_subject,
                    household_member=household_member,
                    report_datetime=datetime.today())

        if status == 'RESEARCH':
            if not household_member.member_status == status:
                # set status
                household_member.member_status = status
                household_member.save()
        # if anything other than RESEARCH and NOT_ELIGIBLE, clear eligibility flag and change
        elif status in [item[0] for item in HOUSEHOLD_MEMBER_ACTION if item[0] not in ['RESEARCH', 'NOT_ELIGIBLE']]:
            if not household_member.member_status == status:
                # clear eligibility flag then set status
                household_member.eligible_subject = False
                household_member.member_status = status
                household_member.save()
        elif household_member.eligible_subject and status == 'NOT_ELIGIBLE':
            # do not allow to change to NOT ELIGIBLE if already has passed eligibility
            pass
        else:
            pass
    return household_member.member_status
