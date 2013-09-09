from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from bhp_base_form.forms import BaseModelForm
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError
from bcpp_household.models import Household
#site_mapper.autodiscover()


def get_mapper():
    mapper = site_mappers.get(settings.CURRENT_COMMUNITY)
    if not mapper:
        raise MapperError('Mapper not registered for community {0}.'.format(settings.CURRENT_COMMUNITY))
    return mapper()


class HouseholdForm(BaseModelForm):

#    community = forms.ChoiceField(
#        label=u'Community',
#        initial=get_mapper().get_map_area(),
#        choices=((get_mapper().get_map_area(), get_mapper().get_map_area()), ),
#        help_text=u'If the community is incorrect, please contact the DMC immediately.',
#        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer, attrs={'class': 'radiolist'}),
#        )

#    section = forms.ChoiceField(
#        label=u'Section',
#        #initial=get_mapper().get_region(),
#        choices=get_mapper().get_regions_as_choices(),
#        help_text=u'',
#        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer, attrs={'class': 'radiolist'}),
#        )
#
#    sub_section = forms.ChoiceField(
#        label=u'Sub-section',
#        choices=get_mapper().get_sections_as_choices(),
#        help_text=u'',
#        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer, attrs={'class': 'radiolist'}),
#        )

    def clean(self):
        cleaned_data = self.cleaned_data
        # check if supplied old identifier is already in sue
        #old_household_identifier = cleaned_data.get('old_household_identifier', None)
        #if old_household_identifier:
        #    if Household.objects.filter(household_identifier=old_household_identifier).exists():
        #        raise forms.ValidationError("{0} already exists".format(old_household_identifier))
        #if not cleaned_data.get('gps_point_1') == '24':
        #    raise forms.ValidationError('GPS S must be 24. Got %s' % (cleaned_data.get('gps_point_1'),))
        #if not cleaned_data.get('gps_point_2') == '26':
        #    raise forms.ValidationError('GPS E must be 26. Got %s' % (cleaned_data.get('gps_point_2'),))

        return cleaned_data

    class Meta:
        model = Household
