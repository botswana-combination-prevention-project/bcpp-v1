from django.conf import settings

from edc.dashboard.search.classes import BaseSearch

from ..forms import GpsSearchForm
from ..models import Plot


class PlotSearchByGps(BaseSearch):

    name = 'plot_gps'
    search_model = Plot
    order_by = 'plot_identifier'
    search_type = 'gps'
    template = 'search_plot_result_include.html'
    form = GpsSearchForm

    def get_most_recent_query_options(self):
        return {'community': settings.CURRENT_COMMUNITY}

    def get_plots_for_community(self):
        return Plot.objects.filter(**{self.get_mapper().map_area_field_attr: self.get_current_community()})

    def get_plots_ordered_by_distance(self, plots, lat, lon, radius):
        """Returns a dictionary of plots and a list of keys in order.

        The dictionary keys are the calculated distance from a given point."""
        ordered_list_of_keys = []
        plots = {}
        for plot in plots:
            plot_distance_from_gps = self.get_mapper().gps_distance_between_points(lat, lon, plot.gps_target_lat, plot.gps_target_lon, radius)
            if plot_distance_from_gps <= radius:
                while plot_distance_from_gps in ordered_list_of_keys:
                    plot_distance_from_gps += .0001  # slightly adjust so no two are the same
                ordered_list_of_keys.append(plot_distance_from_gps)
                plot.relative_distance = plot_distance_from_gps
                plots.update({plot_distance_from_gps: plot})
        ordered_list_of_keys.sort()
        return plots, ordered_list_of_keys

    def get_search_result(self, request, **kwargs):
        search_result = None
        if request.method == 'POST':
            gps_form = self.get_form(request.POST)
            if gps_form.is_valid():
                search_result = []
                radius = gps_form.cleaned_data.get('radius') / 1000
                lat = self.get_mapper().get_gps_lat(gps_form.cleaned_data.get('degrees_s'), float('{0}'.format(gps_form.cleaned_data.get('minutes_s'))))
                lon = self.get_mapper().get_gps_lon(gps_form.cleaned_data.get('degrees_e'), float('{0}'.format(gps_form.cleaned_data.get('minutes_e'))))
                plots, ordered_list_of_keys = self.get_plots_ordered_by_distance(self.get_plots_for_community(), lat, lon, radius)
                for plot_distance_from_gps in ordered_list_of_keys:
                    search_result.append(plots[plot_distance_from_gps])
                request.session['search_result'] = search_result
        elif request.GET.get('plot'):
            search_result = []
            searched_plot = Plot.objects.filter(plot_identifier=request.GET.get('plot'))
            lat = searched_plot[0].gps_target_lat
            lon = searched_plot[0].gps_target_lon
            radius = 1
            plots, ordered_list_of_keys = self.get_plots_ordered_by_distance(searched_plot, lat, lon, radius)
            for plot_distance_from_gps in ordered_list_of_keys:
                search_result.append(plots[plot_distance_from_gps])
            request.session['search_result'] = search_result
        else:
            if request.GET.get('page'):
                search_result = request.session.get('search_result')
        return search_result
