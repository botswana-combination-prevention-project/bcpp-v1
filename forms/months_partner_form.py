from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner
from bcpp.choices import FIRSTPARTNERHIV_CHOICE, YES_NO_UNSURE


class BaseMonthsPartnerForm (BaseSubjectModelForm):

    def clean(self):
        """Ensures that question about antiretrovirals is not answered if partner is known to be HIV negative."""
        cleaned_data = super(MonthsRecentPartnerForm, self).clean()
        # check tuples have not changed
        options = ['Yes', 'No', 'not sure', 'Don\'t want to answer']
        self.options_in_tuple(YES_NO_UNSURE, options)
        self.options_in_tuple(FIRSTPARTNERHIV_CHOICE, ['negative', 'I am not sure'])
        if cleaned_data.get('firstpartnerhiv') == 'negative' and cleaned_data.get('firsthaart') in options:
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and cleaned_data.get('firsthaart') in options:
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        return cleaned_data


class MonthsRecentPartnerForm(BaseMonthsPartnerForm):

    class Meta:
        model = MonthsRecentPartner


class MonthsSecondPartnerForm(BaseMonthsPartnerForm):

    class Meta:
        model = MonthsSecondPartner


class MonthsThirdPartnerForm(BaseMonthsPartnerForm):

    class Meta:
        model = MonthsThirdPartner
