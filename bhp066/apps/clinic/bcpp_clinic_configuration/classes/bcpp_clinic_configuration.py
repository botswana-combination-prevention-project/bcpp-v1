from datetime import datetime
from django.db.models import get_model

from edc.apps.app_configuration.classes import BaseAppConfiguration
# from edc.core.bhp_content_type_map.models import ContentTypeMap


class BcppClinicConfiguration(BaseAppConfiguration):

    appointment_configuration = {
                'allowed_iso_weekdays': '1234567',
                'use_same_weekday': True,
                'default_appt_type': 'default'}

    study_variables_setup = {
                'protocol_number': 'BHP066',
                'protocol_code': '066',
                'protocol_title': 'BCPP Clinic',
                'research_title': 'Botswana Combination Prevention Project - Clinic',
                'study_start_datetime': datetime(2013, 12, 16, 10, 30, 00),
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
                'name': 'clinic',
#                 'content_type_map': '',
                'consent_type': 'sub-study',
                'version': 1,
                'start_datetime': datetime(2013, 12, 16, 10, 30, 00),
                'end_datetime': datetime(2014, 12, 23, 16, 30, 00),
                'add_for_app': 'bcpp_clinic'}

    consent_catalogue_list = [consent_catalogue_setup]