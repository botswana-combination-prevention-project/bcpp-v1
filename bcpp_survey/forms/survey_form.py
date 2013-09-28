from django import forms
from ..models import Survey


class SurveyForm(forms.Form):
    survey = forms.ChoiceField(
        choices=[[survey.survey_name, survey.survey_name] for survey in Survey.objects.all()],
        label="Survey ",
        initial=None,
        help_text="",
        )
