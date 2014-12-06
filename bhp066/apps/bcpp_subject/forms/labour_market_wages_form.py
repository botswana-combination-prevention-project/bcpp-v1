from django import forms
from django.forms.util import ErrorList
from ..models import LabourMarketWages
from .base_subject_model_form import BaseSubjectModelForm

from ..choices import MONTHLY_INCOME, HOUSEHOLD_INCOME


class LabourMarketWagesForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(LabourMarketWagesForm, self).clean()
        grant = self.cleaned_data.get('grant')
        # if yes, answer next question
        if cleaned_data.get('govt_grant') == 'Yes':
            if not grant:
                raise forms.ValidationError('You are to answer questions about Grant')
        return cleaned_data

        employed = ['government sector', 'private sector', 'self-employed working on my own',
                    'self-employed with own employees']
        employed_none = ['occupation', 'monthly_income', 'salary_payment']
        if cleaned_data.get('employed') in employed:
            for response in employed_none:
                if cleaned_data.get(response) == 'None':
                    self._errors[response] = ErrorList[(u'The field cannot be none')]
                    raise forms.ValidationError(
                    'If participant is employed. The response cannot be None')

        monthly_answer = 0
        for i in range(len(MONTHLY_INCOME)):
            if MONTHLY_INCOME[i][1] == cleaned_data.get('monthly_income'):
                monthly_answer = i
                break
        household_answer = 0
        for j in range(len(HOUSEHOLD_INCOME)):
            if HOUSEHOLD_INCOME[j][1] == cleaned_data.get('household_income'):
                household_answer = j
                break
        if monthly_answer > household_answer:
            raise forms.ValidationError(
                    'Amount in household cannot be less than monthly income')

    class Meta:
        model = LabourMarketWages
