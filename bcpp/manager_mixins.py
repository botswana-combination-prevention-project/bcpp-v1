from django.apps import apps as django_apps

from edc_map.site_mappers import site_mappers
from edc_device.constants import CLIENT

from .models import AvailablePlot

app_config = django_apps.get_app_config('bcpp')
edc_device_app_config = django_apps.get_app_config('edc_device')


class CurrentCommunityManagerError(Exception):
    pass


class CurrentCommunityManagerMixin:

    lookup = ['household_structure', 'household', 'plot']
    lookup_sep = '__'

#     def get_queryset(self):
#         if app_config.use_current_community_filter:
#             try:
#                 community = site_mappers.current_mapper.map_area
#             except AttributeError as e:
#                 raise CurrentCommunityManagerError(
#                     'Mapper must return a valid community if \'app_config.use_current_community_filter\' == True. '
#                     'Got {}'.format(str(e)))
#             options = {self.lookup_sep.join(*(self.lookup + ['community'])): community}
#             if edc_device_app_config.role == CLIENT:
#                 available_plots = []
#                 for obj in AvailablePlot.objects.filter(community=community, device_id=edc_device_app_config.device_id):
#                     available_plots.append(obj.plot_identifier)
#                 if available_plots:
#                     options.update({self.lookup_sep.join(*(self.lookup + ['plot_identifier', 'in'])): available_plots})
#             return super(CurrentCommunityManagerMixin, self).get_queryset().filter(**options)
#         return super(CurrentCommunityManagerMixin, self).get_queryset()
