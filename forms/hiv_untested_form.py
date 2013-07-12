from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivUntested


class HivUntestedForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        # if no, don't answer next question
        if cleaned_data.get('hiv_pills') == 'No' and  cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('You are answering information about ARV\'s yet have answered \'NO\', patient has never heard about ARV\'s. Please correct')
        if cleaned_data.get('hiv_pills') == 'Yes' or cleaned_data.get('hiv_pills') == 'not sure' and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('if "%s", answer whether participant believes that HIV positive can live longer if taking ARV\'s. (Q Supplemental HT6)')

        return cleaned_data

    class Meta:
        model = HivUntested
