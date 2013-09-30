from datetime import datetime
from django.contrib.auth.decorators import login_required
from apps.bcpp_dashboard.views import household_dashboard
from apps.bcpp_household_member.forms import ParticipationForm
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry


@login_required
def participation(request, **kwargs):
    """Updates the member status and redirects to the household dashboard."""
    household_member = None
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('household_member')
            household_member = HouseholdMember.objects.get(pk=pk)
            status = form.cleaned_data.get('status', None)
            if household_member.is_consented:
                status = 'CONSENTED'
                if not household_member.member_status == status:
                    household_member.member_status = status
                    household_member.save()
            else:
                if status:
                    if not household_member.member_status == status:
                        household_member.member_status = status
                        household_member.save()
            if status == 'ABSENT':
                #SubjectAbsentee = models.get_model('bcpp_subject', 'subjectabsentee')
                if not SubjectAbsentee.objects.filter(household_member=household_member):
                    SubjectAbsentee.objects.create(
                        registered_subject=household_member.registered_subject,
                        household_member=household_member,
                        report_datetime=datetime.today())
                else:
                    # if no log entries, update the report datetime on the absentee master record.
                    subject_absentee = SubjectAbsentee.objects.get(household_member=household_member)
                    if not SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee):
                        subject_absentee.report_datetime = household_member.modified
#             if status == 'UNDECIDED':
#                 if not SubjectUndecided.objects.filter(household_member=household_member):
#                     SubjectUndecided.objects.create(
#                         registered_subject=household_member.registered_subject,
#                         household_member=household_member,
#                         report_datetime=datetime.today())
#                 else:
#                     # if no log entries, update the report datetime on the undecided master record.
#                     subject_undecided = SubjectUndecided.objects.get(household_member=household_member)
#                     if not SubjectUndecidedEntry.objects.filter(subject_undecided=subject_undecided):
#                         subject_undecided.report_datetime = household_member.modified
    return household_dashboard(request,
        dashboard_type='household',
        dashboard_model='household_structure',
        dashboard_id=household_member.household_structure.pk,
        #household_member=household_member,
        )
