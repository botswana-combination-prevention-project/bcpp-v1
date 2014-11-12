from datetime import datetime, time

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc.map.classes import Mapper
from edc.map.choices import ICONS, OTHER_ICONS

from apps.bcpp_survey.models import Survey

from ..choices import NON_RESIDENTIAL
from ..models import Plot


class BasePlotMapper(Mapper):

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

    item_target_field = 'target'
    item_selected_field = 'selected'

    gps_degrees_s_field_attr = 'gps_degrees_s'
    gps_degrees_e_field_attr = 'gps_degrees_e'
    gps_minutes_s_field_attr = 'gps_minutes_s'
    gps_minutes_e_field_attr = 'gps_minutes_e'

    def __init__(self):
        self.intervention_code = 'CPC' if self.intervention else 'ECC'
        self.verify_survey_dates()

    def __repr__(self):
        return '{}(\'{}\')'.format(self.__class__.__name__, self.map_area)

    def __str__(self):
        return '{}{} ({})'.format(self.map_area[0].upper(), self.map_area[1:], self.intervention_code)

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
        """Verifies that the dates fall within the survey."""
        for survey_slug, survey_dates in self.survey_dates.iteritems():
            try:
                bhs_start_datetime = datetime.combine(survey_dates.bhs_start_date, time.min)
                Survey.objects.current_survey(
                    report_datetime=bhs_start_datetime,
                    survey_slug=survey_slug,
                    datetime_label='bhs_start_datetime')
                bhs_full_enrollment_datetime = datetime.combine(
                    survey_dates.bhs_full_enrollment_date, time.min)
                Survey.objects.current_survey(
                    report_datetime=bhs_full_enrollment_datetime,
                    survey_slug=survey_slug,
                    datetime_label='bhs_full_enrollment_date')
                bhs_end_datetime = datetime.combine(survey_dates.bhs_end_date, time.min)
                Survey.objects.current_survey(
                    report_datetime=bhs_end_datetime,
                    survey_slug=survey_slug,
                    datetime_label='bhs_end_datetime')
            except Survey.DoesNotExist:
                raise ImproperlyConfigured('Date does not fall within defined Survey instance. '
                                           'See mapper and Survey for {}.'.format(survey_slug))

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
        try:
            plot = Plot.objects.get(plot_identifier=self.clinic_plot_identifier)
        except Plot.DoesNotExist:
            plot = Plot.objects.create(
                plot_identifier=self.clinic_plot_identifier,
                household_count=1,
                status='bcpp_clinic',
                community=self.map_area,
                action='confirmed',
                description='BCPP Community Clinic')
        return plot

    @property
    def clinic_plot_identifier(self):
        if not self.map_code:
            raise TypeError('Expected a value for mapper.map_code, Got None.')
        return '{}0000-00'.format(self.map_code)
