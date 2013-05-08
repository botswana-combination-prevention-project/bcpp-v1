from datetime import datetime
from django.contrib.auth.decorators import login_required
from bcpp_dashboard.views import dashboard
from bcpp_dashboard.forms import ParticipationForm
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry


@login_required
def participation(request, **kwargs):
    """Updates the member status and redirects to the household dashboard."""
    household_structure_member = None
    household_identifier = None
    survey = None
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            survey = form.cleaned_data.get('survey')
            pk = form.cleaned_data.get('household_structure_member')
            household_structure_member = HouseholdStructureMember.objects.get(pk=pk)
            household_identifier = household_structure_member.household_structure.household.household_identifier
            status = form.cleaned_data.get('status', None)
            if household_structure_member.is_consented:
                status = 'CONSENTED'
                if not household_structure_member.member_status == status:
                    household_structure_member.member_status = status
                    household_structure_member.save()
            else:
                if status:
                    if not household_structure_member.member_status == status:
                        household_structure_member.member_status = status
                        household_structure_member.save()
            if status == 'ABSENT':
                #SubjectAbsentee = models.get_model('bcpp_subject', 'subjectabsentee')
                if not SubjectAbsentee.objects.filter(household_structure_member=household_structure_member):
                    SubjectAbsentee.objects.create(
                        registered_subject=household_structure_member.registered_subject,
                        household_structure_member=household_structure_member,
                        report_datetime=datetime.today())
                else:
                    # if no log entries, update the report datetime on the absentee master record.
                    subject_absentee = SubjectAbsentee.objects.get(household_structure_member=household_structure_member)
                    if not SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee):
                        subject_absentee.report_datetime = household_structure_member.modified
#             if status == 'UNDECIDED':
#                 if not SubjectUndecided.objects.filter(household_structure_member=household_structure_member):
#                     SubjectUndecided.objects.create(
#                         registered_subject=household_structure_member.registered_subject,
#                         household_structure_member=household_structure_member,
#                         report_datetime=datetime.today())
#                 else:
#                     # if no log entries, update the report datetime on the undecided master record.
#                     subject_undecided = SubjectUndecided.objects.get(household_structure_member=household_structure_member)
#                     if not SubjectUndecidedEntry.objects.filter(subject_undecided=subject_undecided):
#                         subject_undecided.report_datetime = household_structure_member.modified
    return dashboard(request,
        dashboard_type='household',
        household_identifier=household_identifier,
        household_structure_member=household_structure_member,
        survey=survey,
        )
