from datetime import datetime, time

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc_map.classes import Mapper
from edc.map.choices import ICONS, OTHER_ICONS
from edc_device import device

from bhp066.apps.bcpp_survey.models import Survey

from ..models import Plot


class BasePlotMapper(Mapper):

    map_code = None
    map_area = None
    pair = None

    item_model = Plot
    item_model_cls = Plot
    item_label = 'Plot'

    region_field_attr = 'section'
    region_label = 'Section'
    section_field_attr = 'sub_section'
    section_label = 'Sub Section'
    map_area_field_attr = 'community'

    # different map fields, the numbers are the zoom levels
    map_field_attr_18 = 'uploaded_map_18'
    map_field_attr_17 = 'uploaded_map_17'
    map_field_attr_16 = 'uploaded_map_16'

    target_gps_lat_field_attr = 'gps_target_lat'
    target_gps_lon_field_attr = 'gps_target_lon'
    icons = ICONS
    other_icons = OTHER_ICONS

    identifier_field_attr = 'plot_identifier'
    identifier_field_label = 'plot'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    item_target_field = 'bhs'
    item_selected_field = 'selected'

    gps_degrees_s_field_attr = 'gps_degrees_s'
    gps_degrees_e_field_attr = 'gps_degrees_e'
    gps_minutes_s_field_attr = 'gps_minutes_s'
    gps_minutes_e_field_attr = 'gps_minutes_e'

    map_area = None
    map_code = None
    regions = None
    sections = None

    landmarks = None

    intervention = None

    gps_center_lat = None
    gps_center_lon = None
    radius = None
    location_boundary = None

    current_survey_in_settings = settings.CURRENT_SURVEY

    def __init__(self):
        self.active = None
        if self.intervention is None:
            self.intervention_code = None
        else:
            self.intervention_code = 'CPC' if self.intervention else 'ECC'
        if settings.CURRENT_COMMUNITY == self.map_area:
            self.active = True

    def __repr__(self):
        return '{}(\'{}\')'.format(self.__class__.__name__, self.map_area)

    def __str__(self):
        return '{}{} ({}){}'.format(self.map_area[0].upper(), self.map_area[1:], self.intervention_code,
                                    ' *active' if self.active else '')

    @property
    def __dict__(self):
        return {
            'map_area': self.map_area,
            'map_code': self.map_code,
            'gps_center_lat': self.gps_center_lat,
            'gps_center_lon': self.gps_center_lon,
            'radius': self.radius,
            'intervention': self.intervention,
            'survey_dates': self.survey_dates,
            'clinic_days': self.clinic_days}

    def verify_survey_dates(self):
        """Verifies that the dates fall within the survey for the current community."""
        for survey_slug, survey_dates in self.survey_dates.iteritems():
            try:
                if self.active and survey_slug == settings.CURRENT_SURVEY:
                    start_datetime = datetime.combine(survey_dates.start_date, time.min)
                    Survey.objects.current_survey(
                        report_datetime=start_datetime,
                        survey_slug=survey_slug,
                        datetime_label='start_datetime',
                        community=self.map_area)
                    full_enrollment_datetime = datetime.combine(
                        survey_dates.full_enrollment_date, time.min)
                    Survey.objects.current_survey(
                        report_datetime=full_enrollment_datetime,
                        survey_slug=survey_slug,
                        datetime_label='full_enrollment_date',
                        community=self.map_area)
                    end_datetime = datetime.combine(survey_dates.end_date, time.min)
                    Survey.objects.current_survey(
                        report_datetime=end_datetime,
                        survey_slug=survey_slug,
                        datetime_label='end_datetime',
                        community=self.map_area)
            except Survey.DoesNotExist:
                raise ImproperlyConfigured('Date does not fall within defined Survey instance. '
                                           'See mapper and Survey for {}.'.format(survey_slug))
            except ImproperlyConfigured as err_message:
                raise ImproperlyConfigured('{}:{} survey {}. {}'.format(self.map_code, self.map_area,
                                                                        settings.CURRENT_SURVEY,
                                                                        err_message))

    @property
    def test_location(self):
        """Decimal Degrees = Degrees + minutes/60 + seconds/3600"""
        degrees_e, minutes_e = self.deg_to_dms(self.gps_center_lon)
        degrees_s, minutes_s = self.deg_to_dms(self.gps_center_lat)
        return (degrees_s, minutes_s, degrees_e, minutes_e)

    @property
    def current_survey_slug(self):
        """Returns the survey_slug from the Survey instance using settings.CURRENT_SURVEY."""
        return Survey.objects.current_survey(survey_slug=settings.CURRENT_SURVEY).survey_slug

    @property
    def current_survey_dates(self):
        return self.survey_dates.get(self.current_survey_slug)

    @property
    def current_clinic_days(self):
        return self.clinic_days.get(self.current_survey_slug)

    @property
    def clinic_plot(self):
        """Returns and, if needed, creates a non-residential plot to represent the CLINIC."""
        # We can only do this on community servers, not on netbooks or central server.
        try:
            plot = Plot.objects.get(plot_identifier=self.clinic_plot_identifier)
        except Plot.DoesNotExist:
            if device.is_community_server:
                plot = Plot.objects.create(
                    plot_identifier=self.clinic_plot_identifier,
                    household_count=1,
                    status='bcpp_clinic',
                    community=self.map_area,
                    action='confirmed',
                    description=('{} clinic').format(self.map_area))
            else:
                plot = Plot(
                    plot_identifier=self.clinic_plot_identifier,
                    household_count=1,
                    status='bcpp_clinic',
                    community=self.map_area,
                    action='confirmed',
                    description=('{} clinic').format(self.map_area))
        return plot

    @property
    def clinic_plot_identifier(self):
        if not self.map_code:
            raise TypeError('Expected a value for mapper.map_code, Got None.')
        return '{}0000-00'.format(self.map_code)

    @property
    def community(self):
        return self.map_area
