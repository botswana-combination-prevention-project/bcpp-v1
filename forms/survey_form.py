from django import forms
from bhp_map.classes import site_mapper
site_mapper.autodiscover()


class SurveyForm(forms.Form):
    survey = forms.ChoiceField(
        choices=site_mapper.get_mapper_as_tuple(),
        label="Survey: ",
        initial=None,
        help_text="",
        )
