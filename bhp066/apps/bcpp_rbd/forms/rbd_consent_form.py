from dateutil.relativedelta import relativedelta

from django import forms

from edc.core.bhp_variables.models import StudySpecific

from apps.bcpp_subject.forms import MainConsentForm

from ..models import RBDConsent, RBDEligibility


class RBDConsentForm(MainConsentForm):

    def check_elligibility_filled(self, cleaned_data):
        if not cleaned_data.get('household_member').eligible_rbd_subject == True:
            raise forms.ValidationError('Subject is not eligible or has not been confirmed eligible. Complete the eligibility checklist first. Got {0}'.format(cleaned_data.get('household_member')))

    def clean(self):
        try:
            obj = StudySpecific.objects.all()[0]
        except IndexError:
            raise forms.ValidationError("Please contact your DATA/IT assistant to add your edc.core.bhp_variables site specifics")
        cleaned_data = self.cleaned_data
        household_member = cleaned_data.get("household_member")
        #The next checks verify the data is identical to that entered in the enrollment checklist for BHS
        if RBDEligibility.objects.filter(household_member = household_member).exists():
            rbd_eligibility_checklist = RBDEligibility.objects.get(household_member = household_member)
            self.enrollment_checklist_checks(rbd_eligibility_checklist, cleaned_data, obj)
#     def study_specifics_checks(self, obj, cleaned_data):
#         consent_datetime = cleaned_data.get('consent_datetime').date()
#         rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
#         if rdelta.years < obj.minimum_age_of_consent:
#             raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(rdelta.years))
        return super(RBDConsentForm, self).clean()

    class Meta:
        model = RBDConsent
