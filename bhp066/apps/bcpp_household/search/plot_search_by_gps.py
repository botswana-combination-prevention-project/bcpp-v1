from edc.dashboard.search.classes import BaseSearcher
from edc.map.classes import site_mappers

from ..forms import GpsSearchForm
from ..models import Plot
from ..constants import CONFIRMED


class PlotSearchByGps(BaseSearcher):

    name = 'gps'
    search_model = Plot
    order_by = ['plot_identifier']
    template = 'search_plot_result_include.html'
    search_form = GpsSearchForm

    def contribute_to_context(self, context):
        context = super(PlotSearchByGps, self).contribute_to_context(context)
        context.update({'CONFIRMED': CONFIRMED,
                        'gps_search_form': self.search_form})
        return context

    def get_most_recent_query_options(self):
        """Returns a dictionary to be added to the options for filtering the search model."""
        return {'community': site_mappers.current_mapper.map_area}

    def search_result(self, request, **kwargs):
        """Returns an iterable search_result ordered by distance from a given gps point."""
        search_result = []
        gps_form = self.search_form(request.POST)
        mapper = site_mappers.current_mapper
        if gps_form.is_valid():
            radius = gps_form.data.get('radius') / 1000
            lat = mapper().get_gps_lat(gps_form.data.get('degrees_s'), float('{0}'.format(gps_form.data.get('minutes_s'))))
            lon = mapper().get_gps_lon(gps_form.data.get('degrees_e'), float('{0}'.format(gps_form.data.get('minutes_e'))))
            items_as_dct, ordered_list_of_keys = self.get_items_ordered_by_distance(self.search_queryset(), lat, lon, radius)
            for distance_from_gps in ordered_list_of_keys:
                search_result.append(items_as_dct[distance_from_gps])
        return search_result

    def search_queryset(self, request=None):
        """Returns a filtered search model queryset."""
        mapper = site_mappers.current_mapper
        options = {mapper().map_area_field_attr: mapper.map_area}
        if request:
            search_attrvalue = request.GET.get(self.get_search_attrname())  # e.g. identifier
            if search_attrvalue:
                options.update({self.get_search_attrname(): search_attrvalue})
        return self.get_search_model_cls().objects.filter(**{mapper.map_area_field_attr: mapper.map_area})

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
        mapper = site_mappers.current_mapper
        for item in queryset:
            distance_from_gps = mapper().gps_distance_between_points(lat, lon, item.gps_target_lat, item.gps_target_lon)
            if distance_from_gps <= radius:
                while distance_from_gps in ordered_list_of_keys:
                    distance_from_gps += .0001  # slightly adjust so no two are the same
                ordered_list_of_keys.append(distance_from_gps)
                item.relative_distance = distance_from_gps
                items.update({distance_from_gps: item})
        ordered_list_of_keys.sort()
        return items, ordered_list_of_keys
