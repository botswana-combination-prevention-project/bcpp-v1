from django import forms
from edc_map.site_mappers import site_mappers


class SurveyForm(forms.Form):
    survey = forms.ChoiceField(
        choices=site_mappers.map_areas,
        label="Survey: ",
        initial=None,
        help_text="",
    )
