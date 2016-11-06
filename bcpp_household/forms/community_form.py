from django import forms

from edc_map.site_mappers import site_mappers


class CommunityForm(forms.Form):
    community = forms.ChoiceField(
        choices=site_mappers.map_areas,
        label="Community",
        initial=None,
        help_text="",
    )
