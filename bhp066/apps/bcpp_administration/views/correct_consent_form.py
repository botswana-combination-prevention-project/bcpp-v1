from datetime import date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render_to_response
from django.template import RequestContext

from ..forms import CorrectConsentForm

from apps.bcpp_subject.models import SubjectConsent
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import EnrollmentChecklist


def correct_consent_form(request):
    """Corrects the consent values."""

    if request.method == 'POST':
        form = CorrectConsentForm(request.POST)
        if form.is_valid():
            subject_identifier = form.cleaned_data.get('subject_identifier')
            last_name = form.cleaned_data.get('lastname')
            first_name = form.cleaned_data.get('firstname')
            initials = form.cleaned_data.get('initials')
            dob = form.cleaned_data.get('dob')
            gender = form.cleaned_data.get('gender')
            guardian_name = form.cleaned_data.get('guardian_name')
            is_literate = form.cleaned_data.get('is_literate')
            may_store_samples = form.cleaned_data.get('may_store_samples')
            consent_form_dict = {
                    'subject_identifier': subject_identifier,
                    'last_name': last_name,
                    'first_name': first_name,
                    'initials': initials,
                    'dob': dob,
                    'gender': gender,
                    'guardian_name': guardian_name,
                    'is_literate': is_literate,
                    'may_store_samples': may_store_samples}
            consent = SubjectConsent.objects.get(subject_identifier=subject_identifier)
            household_member = HouseholdMember.objects.get(id=consent.household_member_id)
            erollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
            erollment_checklist.update_values = True
            erollment_checklist.save()
            household_member_fields = []
            consent_fields = []
            enrollment_fields = []
            for field in HouseholdMember._meta.fields:
                household_member_fields.append(field.name)
            for field in EnrollmentChecklist._meta.fields:
                enrollment_fields.append(field.name)
            for field in SubjectConsent._meta.fields:
                consent_fields.append(field.name)

            for key, value in consent_form_dict.iteritems():
                if value:
                    if key in household_member_fields:
                        household_member.key = value
                        household_member.save()
                    if key == 'dob':
                        age_in_years = relativedelta(date.today(), dob).years
                        household_member.age_in_years = age_in_years
                        household_member.save()
            household_member = HouseholdMember.objects.get(id=consent.household_member_id)
            erollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
            for key, value in consent_form_dict.iteritems():
                if value:
                    if key in enrollment_fields:
                        erollment_checklist.key = value
                        erollment_checklist.save()
            consent = SubjectConsent.objects.get(subject_identifier=subject_identifier)
            for key, value in consent_form_dict.iteritems():
                if value:
                    if key in consent_fields and not key == 'subject_identifier':
                        consent.key = value
                        consent.save()
            template = 'correct_data_index.html'
            return render_to_response(
                    template, {
                     },
                    context_instance=RequestContext(request)
                )
