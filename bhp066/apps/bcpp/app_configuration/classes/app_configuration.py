from collections import OrderedDict
from datetime import datetime

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc.map.classes import site_mappers

from lis.labeling.classes import LabelPrinterTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from apps.bcpp_survey.models import Survey

study_start_datetime = datetime(2013, 10, 18, 10, 30, 00)
study_end_datetime = datetime(2014, 10, 17, 16, 30, 00)


class BcppAppConfiguration(BaseAppConfiguration):

    def __init__(self):
        super(BcppAppConfiguration, self).__init__()
        self.update_or_create_survey()

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
            'allow_additional_requisitions': False},
        'appointment':
            {'allowed_iso_weekdays': '1234567',
             'use_same_weekday': True,
             'default_appt_type': 'default',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
        }

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
                'content_type_map': 'subjectconsent',
                'consent_type': 'study',
                'version': 1,
                'start_datetime': study_start_datetime,
                'end_datetime': study_end_datetime,
                'add_for_app': 'bcpp_subject'}

    survey_setup = {
                'bcpp-year-1':
                    {'survey_name': 'BCPP Year 1',
                     'survey_slug': 'bcpp-year-1',
                     'datetime_start': study_start_datetime,
                     'datetime_end': datetime(2014, 10, 29, 16, 30, 00)},
                'bcpp-year-2':
                    {'survey_name': 'BCPP Year 2',
                     'survey_slug': 'bcpp-year-2',
                     'datetime_start': datetime(2014, 10, 30, 07, 00, 00),
                     'datetime_end': datetime(2015, 10, 29, 16, 30, 00)},
                'bcpp-year-3':
                    {'survey_name': 'BCPP Year 3',
                     'survey_slug': 'bcpp-year-3',
                     'datetime_start': datetime(2015, 10, 30, 07, 00, 00),
                     'datetime_end': datetime(2016, 10, 29, 16, 30, 00)}
                }

    study_site_setup = {'site_name': site_mappers.get_current_mapper().map_area,
                        'site_code': site_mappers.get_current_mapper().map_code}

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                  PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Microtube', 'STORAGE', 'WB'),
                  PanelTuple('ELISA', 'TEST', 'WB'),
                  PanelTuple('Venous (HIV)', 'TEST', 'WB'),
                  ],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16')]}

    lab_setup = {'bcpp': {
                     'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                               PanelTuple('Viral Load', 'TEST', 'WB'),
                               PanelTuple('Microtube', 'STORAGE', 'WB'),
                               PanelTuple('ELISA', 'TEST', 'WB'),
                               PanelTuple('Venous (HIV)', 'TEST', 'WB'),
                               ],
                     'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                      AliquotTypeTuple('Plasma', 'PL', '32'),
                                      AliquotTypeTuple('Buffy Coat', 'BC', '16')],
                     'profile': [ProfileTuple('Viral Load', 'WB'), ProfileTuple('Genotyping', 'WB'), ProfileTuple('ELISA', 'WB')],
                     'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                      ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                      ProfileItemTuple('Genotyping', 'PL', 1.0, 4),
                                      ProfileItemTuple('Genotyping', 'BC', 0.5, 2),
                                      ProfileItemTuple('ELISA', 'PL', 1.0, 1),
                                      ProfileItemTuple('ELISA', 'BC', 0.5, 1)]}}

    labeling = {'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', '127.0.0.1', True), ],
#                 'zpl_template': ZplTemplateTuple('aliquot_label', ''),
                }

    consent_catalogue_list = [consent_catalogue_setup]

    export_plan_setup = {'bcpp_subject.subjectreferral': {
        'app_label': 'bcpp_subject',
        'object_name': 'subjectreferral',
        'fields': [],
        'extra_fields': OrderedDict(
            {'plot_identifier': 'subject_visit__household_member__household_structure__household__plot__plot_identifier',
             'dob': 'subject_visit__appointment__registered_subject__dob',
             'first_name': 'subject_visit__appointment__registered_subject__first_name',
             'identity': 'subject_visit__appointment__registered_subject__identity',
             'identity_type': 'subject_visit__appointment__registered_subject__identity_type',
             'initials': 'subject_visit__appointment__registered_subject__initials',
             'last_name': 'subject_visit__appointment__registered_subject__last_name',
             'subject_identifier': 'subject_visit__appointment__registered_subject__subject_identifier',
             }),
        'exclude': [
            'comment',
            'created',
            'exported',
            'hostname_created',
            'hostname_modified',
            'in_clinic_flag',
            'modified',
            'referral_clinic_other',
            'revision',
            'subject_visit',
            'user_created',
            'user_modified',
             ],
        'header': True,
        'track_history': True,
        'show_all_fields': True,
        'delimiter': '|',
        'encrypt': False,
        'strip': True,
        'target_path': '~/export_to_cdc'
        }}

    def update_or_create_survey(self):
        for survey_values in self.survey_setup.itervalues():
            if not Survey.objects.filter(survey_name=survey_values.get('survey_name')):
                Survey.objects.create(**survey_values)
            else:
                survey = Survey.objects.get(survey_name=survey_values.get('survey_name'))
                survey.survey_slug = survey_values.get('survey_slug')
                survey.datetime_start = survey_values.get('datetime_start')
                survey.datetime_end = survey_values.get('datetime_end')
                survey.save()
