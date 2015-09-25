from django import forms

from edc_constants.constants import NOT_APPLICABLE

from bhp066.apps.bcpp.choices import FIRSTPARTNERHIV_CHOICE, YES_NO_UNSURE

from ..models import MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner

from .base_subject_model_form import BaseSubjectModelForm


class BaseMonthsPartnerForm (BaseSubjectModelForm):

    yes_no_unsure_options = ['Yes', 'No', 'not sure', 'Don\'t want to answer']

    def check_tuples(self):
        # check tuples have not changed
        self.options_in_tuple(YES_NO_UNSURE, self.yes_no_unsure_options)
        self.options_in_tuple(FIRSTPARTNERHIV_CHOICE, ['negative', 'I am not sure'])

    def clean(self):
        """Ensures that question about antiretrovirals is not answered if partner is known to be HIV negative."""
        cleaned_data = super(BaseMonthsPartnerForm, self).clean()
        if cleaned_data.get('firstpartnerhiv') == 'negative' and cleaned_data.get('firsthaart') in self.yes_no_unsure_options:
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and cleaned_data.get('firsthaart') in self.yes_no_unsure_options:
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        # validating number of months and days
        if cleaned_data.get('third_last_sex', None) == 'Days' and cleaned_data.get('third_last_sex_calc') > 31:
            raise forms.ValidationError('if last time of sex is in days, then days cannot exceed 31')
        if cleaned_data.get('third_last_sex', None) == 'Months' and cleaned_data.get('third_last_sex_calc') > 12:
            raise forms.ValidationError('if last time of sex is in months, then months in a year cannot exceed 12')
        # validating number of months and days
        if cleaned_data.get('first_first_sex', None) == 'Days' and cleaned_data.get('first_first_sex_calc') > 31:
            raise forms.ValidationError('if first time of sex is in days, then days cannot exceed 31')
        if cleaned_data.get('first_first_sex', None) == 'Months' and cleaned_data.get('first_first_sex_calc') > 12:
            raise forms.ValidationError('if first time of sex is in months, then months in a year cannot exceed 12')
        if self.instance.skip_logic_questions(self.cleaned_data.get('first_partner_live')):
            if not cleaned_data.get('sex_partner_community', None) == NOT_APPLICABLE:
                raise forms.ValidationError('if response in question 3, is In this community or Farm within this community or'
                                            'Cattle post within this community. The response in the next question is NOT_APPLICABLE')
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
