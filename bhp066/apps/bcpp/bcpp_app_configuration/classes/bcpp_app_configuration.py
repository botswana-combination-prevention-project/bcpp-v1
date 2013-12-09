from datetime import datetime
from django.db.models import get_model

from edc.apps.app_configuration.classes import BaseAppConfiguration
# from edc.core.bhp_content_type_map.models import ContentTypeMap


class BcppAppConfiguration(BaseAppConfiguration):

    appointment_configuration = {
                'allowed_iso_weekdays': '1234567',
                'use_same_weekday': True,
                'default_appt_type': 'default'}

    study_variables_setup = {
                'protocol_number': 'BHP066',
                'protocol_code': '066',
                'protocol_title': 'BCPP',
                'research_title': 'Botswana Combination Prevention Project',
                'study_start_datetime': datetime(2013, 10, 29, 10, 30, 00),
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
                'name': 'baseline',
                # TO DO: how do we call a ContentTypeMap here???
#                 'content_type_map': '',
                'consent_type': 'study',
                'version': 1,
                'start_datetime': datetime(2013, 10, 29, 10, 30, 00),
                'end_datetime': datetime(2014, 10, 29, 16, 30, 00),
                'add_for_app': 'bcpp_subject'}

    set_survey = {
                'survey_name': 'BCPP Year 1',
                'survey_slug': 'bcpp-year-1',
                'datetime_start': datetime(2013, 10, 29, 10, 30, 00),
                'datetime_end': datetime(2014, 10, 29, 16, 30, 00)}
