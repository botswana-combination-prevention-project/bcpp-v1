from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(SexualBehaviourForm, self).clean()
        #validating having had sex and no sex
        if cleaned_data.get('ever_sex') == 'No' and cleaned_data.get('lifetime_sex_partners') and cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has NEVER had sex, DO NOT provide details about sexual partners')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('lifetime_sex_partners') and not cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has had sex at some point in their life, give details about sexual partners')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('more_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, has participant had sex with anyone outside community?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('first_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, how old was the participant when he/she first had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('condom'):
            raise forms.ValidationError('If participant has had sex at some point in their life, did participant use a condom the last time he/she had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('alcohol_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, did participant drink alcohol before sex last time?')
        
        #validate never having sex
        if cleaned_data.get('ever_sex') == 'No' and cleaned_data.get('more_sex') and cleaned_data.get('first_sex'):
            raise forms.ValidationError('If participant has NEVER had sex, DO NOT any sexual intercourse details')
        if cleaned_data.get('ever_sex') == 'No' and cleaned_data.get('condom') and cleaned_data.get('alcohol_sex'):
            raise forms.ValidationError('If participant has NEVER had sex, DO NOT any other details')
        
        return cleaned_data

    class Meta:
        model = SexualBehaviour
