from datetime import datetime

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.core.bhp_content_type_map.models import ContentTypeMap

from apps.bcpp_survey.models import Survey
from edc.map.classes import site_mappers


study_start_datetime = datetime(2013, 12, 29, 10, 30, 00)
study_end_datetime = datetime(2014, 10, 29, 16, 30, 00)


class BcppAppConfiguration(BaseAppConfiguration):

    def __init__(self):
        super(BcppAppConfiguration, self).__init__()
        self.update_or_create_survey()

    appointment_configuration = {
                'allowed_iso_weekdays': '1234567',
                'use_same_weekday': True,
                'default_appt_type': 'default'}

    study_variables_setup = {
                'protocol_number': 'BHP066',
                'protocol_code': '066',
                'protocol_title': 'BCPP',
                'research_title': 'Botswana Combination Prevention Project',
                'study_start_datetime': study_start_datetime,
                'minimum_age_of_consent': 16,
                'maximum_age_of_consent': 64,
                'gender_of_consent': 'MF',
                'subject_identifier_seed': '10000',
                'subject_identifier_prefix': '066',
                'subject_identifier_modulus': '7',
                'subject_type': 'subject',
                'machine_type': 'SERVER',
                'hostname_prefix': 's030',
                'device_id': '99'}

    consent_catalogue_setup = {
                'name': 'bcpp-year-1',
                # TO DO: how do we call a ContentTypeMap here???
                'content_type_map': ContentTypeMap.objects.get(app_label='bcpp_subject', module_name='subjectconsent'),
                'consent_type': 'study',
                'version': 1,
                'start_datetime': study_start_datetime,
                'end_datetime': study_end_datetime,
                'add_for_app': 'bcpp_subject'}

    rbd_consent_catalogue_setup = {
                'name': 'subject_rbd-year-1',
                # TO DO: how do we call a ContentTypeMap here???
                'content_type_map': ContentTypeMap.objects.get(app_label='bcpp_rbd_subject', module_name='subjectconsentrbdonly'),
                'consent_type': 'study',
                'version': 1,
                'start_datetime': study_start_datetime,
                'end_datetime': study_end_datetime,
                'add_for_app': 'bcpp_rbd_subject'}

    survey_setup = {
                'survey_name': 'BCPP Year 1',
                'survey_slug': 'bcpp-year-1',
                'datetime_start': study_start_datetime,
                'datetime_end': datetime(2014, 10, 29, 16, 30, 00)}

    study_site_setup = {'site_name': site_mappers.get_current_mapper().map_area,
                        'site_code': site_mappers.get_current_mapper().map_code}

    consent_catalogue_list = [consent_catalogue_setup, rbd_consent_catalogue_setup]

    def update_or_create_survey(self):
        if Survey.objects.all().count() == 0:
            Survey.objects.create(**self.survey_setup)
        else:
            try:
                # mat fail on tests if surveys created there
                Survey.objects.all().update(**self.survey_setup)
            except:
                pass