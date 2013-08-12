from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner


class MonthsRecentPartnerForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(MonthsRecentPartnerForm, self).clean()
        # ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data.get('firstpartnerhiv') == 'negative' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        return cleaned_data

    class Meta:
        model = MonthsRecentPartner


class MonthsSecondPartnerForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(MonthsSecondPartnerForm, self).clean()
        # ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data.get('firstpartnerhiv') == 'negative' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        return cleaned_data

    class Meta:
        model = MonthsSecondPartner


class MonthsThirdPartnerForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(MonthsThirdPartnerForm, self).clean()
        # ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data.get('firstpartnerhiv') == 'negative' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and (cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer'):
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        return cleaned_data

    class Meta:
        model = MonthsThirdPartner
