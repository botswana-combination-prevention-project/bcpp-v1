from django.apps import AppConfig as DjangoApponfig

from edc_device.apps import AppConfig as EdcDeviceAppConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent


class AppConfig(DjangoApponfig):
    name = 'bcpp'
    verbose_name = 'Botswana Combination Prevention Project'


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):
    device_id = '99'


class EdcMapAppConfig(EdcMapAppConfigParent):
    verbose_name = 'BCPP Mappers'
    mapper_model = ('bcpp_household', 'plot')
    mapper_survey_model = ('bcpp_survey', 'survey')
    landmark_model = ('bcpp_map', 'landmark')
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']
