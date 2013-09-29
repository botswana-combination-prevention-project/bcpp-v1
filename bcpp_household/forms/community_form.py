from django import forms
from edc_core.bhp_map.classes import site_mappers


class CommunityForm(forms.Form):
    community = forms.ChoiceField(
        choices=site_mappers.get_mapper_as_tuple(),
        label="Community",
        initial=None,
        help_text="",
        )
