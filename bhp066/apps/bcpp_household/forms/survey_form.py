from django import forms
from edc.map.classes import site_mappers


class SurveyForm(forms.Form):
    survey = forms.ChoiceField(
        choices=site_mappers.get_mapper_as_tuple(),
        label="Survey: ",
        initial=None,
        help_text="",
    )
