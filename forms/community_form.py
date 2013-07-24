from django import forms
from bhp_map.classes import site_mappers
site_mappers.autodiscover()


class CommunityForm(forms.Form):
    community = forms.ChoiceField(
        choices=site_mappers.get_mapper_as_tuple(),
        label="Community",
        initial=None,
        help_text="",
        )
