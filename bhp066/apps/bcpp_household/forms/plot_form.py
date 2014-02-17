from django import forms

from edc.base.form.forms import BaseModelForm
from edc.map.classes import site_mappers

from ..models import Plot


class PlotForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance:
            if not self.instance.community:
                raise forms.ValidationError('Community may not be blank. Must be one of {1}.'.format(self.instance.community, ', '.join(site_mappers.get_as_list())))
            if not self.instance.community in site_mappers.get_as_list():
                raise forms.ValidationError('Unknown community {0}. Must be one of {1}.'.format(self.instance.community, ', '.join(site_mappers.get_as_list())))

            # verify gps to target before the save() method does
            if not cleaned_data.get('gps_degrees_s') and not cleaned_data.get('gps_minutes_s') and not cleaned_data.get('gps_degrees_e') and not cleaned_data.get('gps_minutes_e'):
                raise forms.ValidationError('The following fields must all be filled gps_degrees_s, gps_minutes_s, gps_degrees_e, gps_minutes_e. Got {0}, {1}, {2}, {3}'.format(cleaned_data.get('gps_degrees_s'), cleaned_data.get('gps_minutes_s'), cleaned_data.get('gps_degrees_e'), cleaned_data.get('gps_minutes_e')))
            mapper_cls = site_mappers.get_registry(self.instance.community)
            mapper = mapper_cls()
            gps_lat = mapper.get_gps_lat(cleaned_data.get('gps_degrees_s'), cleaned_data.get('gps_minutes_s'))
            gps_lon = mapper.get_gps_lon(cleaned_data.get('gps_degrees_e'), cleaned_data.get('gps_minutes_e'))
            mapper.verify_gps_location(gps_lat, gps_lon, forms.ValidationError)
            mapper.verify_gps_to_target(gps_lat, gps_lon, self.instance.gps_target_lat, self.instance.gps_target_lon, self.instance.target_radius, forms.ValidationError)

        if self.instance.id:
            self.instance.household_count = self.instance.create_or_delete_households(self.instance)
            if self.instance.household_count > 0:
                self.cleaned_data['status'] = 'occupied'

        if not cleaned_data.get('household_count') and cleaned_data.get('status') in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration']:
            raise forms.ValidationError('Invalid number of households for plot that is {0}. Got {1}.'.format(cleaned_data.get('status'), cleaned_data.get('household_count')))

        if (cleaned_data.get('household_count') == 0 and cleaned_data.get('status') in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration']) or (cleaned_data.get('household_count') and not cleaned_data.get('status') in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration']):
            raise forms.ValidationError('Invalid number of households for plot that is {0}. Got {1}.'.format(cleaned_data.get('status'), cleaned_data.get('household_count')))

        if not cleaned_data.get('status') == 'occupied' and cleaned_data.get('eligible_members') > 0:
            raise forms.ValidationError('If the residence is not occupied, number of eligible members should be 0. Got {0}'.format(cleaned_data.get('eligible_members')))

        if cleaned_data.get('status') == 'occupied' and (not cleaned_data.get('time_of_week') or not cleaned_data.get('time_of_day')):
            raise forms.ValidationError('If the residence is occupied, provide the best time to visit (e.g time of week, time of day).')

        if not cleaned_data.get('status') == 'occupied' and (cleaned_data.get('time_of_week') or cleaned_data.get('time_of_day')):
            raise forms.ValidationError('If the residence is NOT occupied, do not provide the best time to visit (e.g time of week, time of day).')
        return cleaned_data

    class Meta:
        model = Plot
