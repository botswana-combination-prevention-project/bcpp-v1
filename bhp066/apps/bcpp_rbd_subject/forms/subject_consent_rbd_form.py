from django import forms
from apps.bcpp_subject.forms import MainConsentForm
from apps.bcpp_rbd_subject.models import SubjectConsentRBDonly

class SubjectConsentRBDForm(MainConsentForm):

    def check_elligibility_filled(self, cleaned_data):
        if not cleaned_data.get('household_member').eligible_rbd_subject == True:
            raise forms.ValidationError('Subject is not eligible or has not been confirmed eligible. Complete the eligibility checklist first. Got {0}'.format(cleaned_data.get('household_member')))

    class Meta:
        model = SubjectConsentRBDonly
