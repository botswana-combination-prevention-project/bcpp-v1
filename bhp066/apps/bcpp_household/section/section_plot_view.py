from django.conf import settings
from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers
from apps.bcpp_survey.forms import SurveyForm
from ..forms.current_gps_form import CurrentGpsForm
from ..models import Plot, Household
from ..forms import CommunityForm


site_mappers.autodiscover()


class SectionPlotView(BaseSectionView):
    section_name = 'plot'
    section_display_name = 'Plots'
    add_model = Plot
    section_display_index = 10
    section_template = 'section_bcpp_plot.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if 'CURRENT_SURVEY' in dir(settings):
            current_survey = settings.CURRENT_SURVEY
            survey_form = None
        else:
            survey_form = SurveyForm()
        context.update({'survey_form': survey_form, 'current_survey': current_survey})
        current_community = None
        if 'CURRENT_COMMUNITY' in dir(settings):
            current_community = settings.CURRENT_COMMUNITY
            community_form = None
        else:
            community_form = CommunityForm()
        gps_search_form = CurrentGpsForm(initial={'community': current_community, 'radius': 100})
        context.update({'community_form': community_form,
                        'current_community': current_community,
                        'mapper_name': current_community,
                        'gps_search_form': gps_search_form})
        return context

    def get_search_result(self, request, **kwargs):
        search_result = None
        if request.method == 'POST':
            gps_form = CurrentGpsForm(request.POST)
            if gps_form.is_valid():
                degrees_s = gps_form.cleaned_data.get('degrees_s')
                degrees_e = gps_form.cleaned_data.get('degrees_e')
                minutes_s = float('{0}'.format(gps_form.cleaned_data.get('minutes_s')))
                minutes_e = float('{0}'.format(gps_form.cleaned_data.get('minutes_e')))
                radius = gps_form.cleaned_data.get('radius') / 1000
                community = settings.CURRENT_COMMUNITY
                mapper = site_mappers.get(community)()
                lat = mapper.get_gps_lat(degrees_s, minutes_s)
                lon = mapper.get_gps_lon(degrees_e, minutes_e)
                search_result = []
                lst = []
                dct = {}
                for plot in Plot.objects.filter(**{mapper.map_area_field_attr: community}):
                    dist = mapper.gps_distance_between_points(lat, lon, plot.gps_target_lat, plot.gps_target_lon, radius)
                    if dist <= radius:
                        plot.relative_distance = dist
                        while dist in lst:
                            dist += .0001
                        lst.append(dist)
                        dct.update({dist: plot})
                lst.sort()
                for dist in lst:
                    search_result.append(dct[dist])
                request.session['search_result'] = search_result
            else:
                self.context.update({'gps_search_form': gps_form})
        else:
            if request.GET.get('page'):
                search_result = request.session['search_result']
        return search_result

site_sections.register(SectionPlotView)
