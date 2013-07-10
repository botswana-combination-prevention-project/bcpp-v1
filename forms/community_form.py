from django import forms
from bhp_map.classes import site_mapper
site_mapper.autodiscover()


class CommunityForm(forms.Form):
    community = forms.ChoiceField(
        choices=site_mapper.get_mapper_as_tuple(),
        label="Community",
        initial=None,
        help_text="",
        )
