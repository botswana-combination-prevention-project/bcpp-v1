from edc.map.classes import site_mappers
from edc.dashboard.search.classes import BaseSearcher

from .base_search_by_mixin import BaseSearchByMixin


class BaseSearchByGps(BaseSearchByMixin, BaseSearcher):

    def __init__(self):
        super(BaseSearchByGps, self).__init__()
        self._mapper = None
        self.set_mapper()

    def set_mapper(self):
        mapper_cls = site_mappers.get_registry(self.get_current_community())
        self._mapper = mapper_cls()

    def get_mapper(self):
        """Returns the mapper instance for this community."""
        return self._mapper

    def contribute_to_context(self, context):
        context.update({'gps_search_form': self.get_search_form()})
        return context

    def get_search_queryset(self, request=None):
        """Returns a filtered search model queryset."""
        options = {self.get_mapper().map_area_field_attr: self.get_current_community()}
        if request:
            search_attrvalue = request.GET.get(self.get_search_attrname())  # e.g. identifier
            if search_attrvalue:
                options.update({self.get_search_attrname(): search_attrvalue})
        return self.get_search_model_cls().objects.filter(**{self.get_mapper().map_area_field_attr: self.get_current_community()})

    def get_items_ordered_by_distance(self, queryset, lat, lon, radius):
        """Returns a dictionary of search items and a list of keys in order.

        The dictionary keys are the calculated distance from a given point.

        The queryset must be from a model that has the following attributes:
            * gps_target_lat
            * gps_target_lon
            * relative_distance
            """
        ordered_list_of_keys = []
        items = {}
        for item in queryset:
            distance_from_gps = self.get_mapper().gps_distance_between_points(lat, lon, item.gps_target_lat, item.gps_target_lon, radius)
            if distance_from_gps <= radius:
                while distance_from_gps in ordered_list_of_keys:
                    distance_from_gps += .0001  # slightly adjust so no two are the same
                ordered_list_of_keys.append(distance_from_gps)
                item.relative_distance = distance_from_gps
                items.update({distance_from_gps: item})
        ordered_list_of_keys.sort()
        return items, ordered_list_of_keys

    def get_search_result(self, request, **kwargs):
        """Returns an iterable search_result ordered by distance from a given gps point."""
        search_result = []
        gps_form = self.get_search_form(request.POST)
        if gps_form.is_valid():
            radius = gps_form.cleaned_data.get('radius') / 1000
            lat = self.get_mapper().get_gps_lat(gps_form.cleaned_data.get('degrees_s'), float('{0}'.format(gps_form.cleaned_data.get('minutes_s'))))
            lon = self.get_mapper().get_gps_lon(gps_form.cleaned_data.get('degrees_e'), float('{0}'.format(gps_form.cleaned_data.get('minutes_e'))))
            items_as_dct, ordered_list_of_keys = self.get_items_ordered_by_distance(self.get_search_queryset(), lat, lon, radius)
            for distance_from_gps in ordered_list_of_keys:
                search_result.append(items_as_dct[distance_from_gps])
        return search_result
