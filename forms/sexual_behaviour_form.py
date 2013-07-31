from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #validating having had sex and no sex
        if cleaned_data.get('ever_sex') == 'No' and cleaned_data.get('lifetime_sex_partners') and cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has NEVER had sex, do not provide details about sexual partners')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('lifetime_sex_partners') and not cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has had sex at some point in their life, give details about sexual partners')

        cleaned_data = super(SexualBehaviourForm, self).clean()
        return cleaned_data

    class Meta:
        model = SexualBehaviour
