from dateutil.parser import parse
from django.apps import AppConfig as DjangoApponfig
from django.conf import settings
from django.utils import timezone

from edc_device.apps import AppConfig as EdcDeviceAppConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_identifier.apps import AppConfig as EdcIdentifierAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint

from bcpp_survey.apps import AppConfig as BcppSurveyAppConfigParent


class AppConfig(DjangoApponfig):
    name = 'bcpp'
    verbose_name = 'Botswana Combination Prevention Project'
    use_current_community_filter = True


class BcppSurveyAppConfig(BcppSurveyAppConfigParent):
    current_survey = None


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):
    device_id = '99'


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    enrollment_caps = {'bcpp_subject.enrollment': ('subject', -1)}
    study_open_datetime = parse('18-OCT-2013 07:00 UTC', tzinfos={'UTC': timezone.get_current_timezone()})


class EdcMapAppConfig(EdcMapAppConfigParent):
    verbose_name = 'BCPP Mappers'
    mapper_model = ('bcpp_household', 'plot')
    mapper_survey_model = ('bcpp_survey', 'survey')
    landmark_model = ('bcpp_map', 'landmark')
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']
    current_mapper_name = settings.CURRENT_MAPPER_NAME


class EdcIdentifierAppConfig(EdcIdentifierAppConfigParent):
    identifier_prefix = '066'


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='bcpp_subject.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='CLOSED'
        )
    ]
