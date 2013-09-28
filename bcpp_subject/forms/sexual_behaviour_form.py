from django import forms
from bcpp_subject.models import SexualBehaviour
from base_subject_model_form import BaseSubjectModelForm


class SexualBehaviourForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(SexualBehaviourForm, self).clean()
        # validating no sex
        self.validate_no_sex('lifetime_sex_partners', cleaned_data)
        self.validate_no_sex('last_year_partners', cleaned_data)
        self.validate_no_sex('more_sex', cleaned_data)
        self.validate_no_sex('first_sex', cleaned_data)
        self.validate_no_sex('condom', cleaned_data)
        self.validate_no_sex('alcohol_sex', cleaned_data)
        # validating having had sex
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('lifetime_sex_partners'):
            raise forms.ValidationError('If participant has had sex at some point in their life, give details about sexual partners')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has had sex at some point in their life, give details about sexual partners')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('more_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, has participant had sex with anyone outside community?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('first_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, how old was the participant when he/she first had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('condom'):
            raise forms.ValidationError('If participant has had sex at some point in their life, did participant use a condom the last time he/she had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('alcohol_sex'):
            raise forms.ValidationError('If participant has had sex at some point in their life, did participant drink alcohol before sex last time?')
        return cleaned_data

    def validate_no_sex(self, field, cleaned_data):
        msg = 'If participant has NEVER had sex, DO NOT provide any other sexual intercourse related questions'
        self.validate_dependent_fields('ever_sex', field, cleaned_data, msg)

    def validate_dependent_fields(self, master_field, sub_field, cleaned_data, msg):
        if cleaned_data.get(master_field, None) == 'No' and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)

    class Meta:
        model = SexualBehaviour
