from dateutil.relativedelta import relativedelta

from django import forms

from apps.bcpp_subject.forms import MainConsentForm

from ..models import RBDConsent


class RBDConsentForm(MainConsentForm):

    def check_elligibility_filled(self, cleaned_data):
        if not cleaned_data.get('household_member').eligible_rbd_subject == True:
            raise forms.ValidationError('Subject is not eligible or has not been confirmed eligible. Complete the eligibility checklist first. Got {0}'.format(cleaned_data.get('household_member')))

    def study_specifics_checks(self, obj, cleaned_data):
        consent_datetime = cleaned_data.get('consent_datetime').date()
        rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
        if rdelta.years < obj.minimum_age_of_consent:
            raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(rdelta.years))

    class Meta:
        model = RBDConsent
