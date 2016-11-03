from django import forms
from dateutil.relativedelta import relativedelta
from datetime import datetime

from bhp066.apps.bcpp.base_model_form import BaseModelForm


from ..models import ClinicEligibility


class ClinicEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicEligibilityForm, self).clean()
        self.validate_guardian()
        try:
            if self.instance.is_consented:
                raise forms.ValidationError('Household member for this checklist has been consented. '
                                            'Eligibility checklist may not be edited')
        except AttributeError:
            pass
        if cleaned_data.get('has_identity') == 'No' and cleaned_data.get('identity'):
            raise forms.ValidationError('You indicated the patient did not provide '
                                        'an identity but identity is provided. Please correct.')
        if cleaned_data.get('has_identity') == 'Yes' and not cleaned_data.get('identity'):
            raise forms.ValidationError('You indicated the patient did has provided '
                                        'an identity but no identity has been provided. Please correct.')
        if cleaned_data.get('identity'):
            if not self.instance:
                self._meta.model.check_for_known_identity(cleaned_data.get('identity'), forms.ValidationError)

        self._meta.model.check_for_consent(cleaned_data.get('identity'), forms.ValidationError)

        return cleaned_data

    def validate_guardian(self):
        if self.cleaned_data.get('guardian') == 'Yes':
            age = relativedelta(datetime.today(), self.cleaned_data.get('dob'))
            if not (age.years in [16, 17]):
                raise forms.ValidationError(
                    "A minor age should be 16 or 17 years. Participart's age today {} years.".format(age.years))

    class Meta:
        model = ClinicEligibility
