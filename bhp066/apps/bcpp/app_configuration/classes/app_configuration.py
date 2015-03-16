from apps.bcpp_household.constants import BASELINE_SURVEY_SLUG
from apps.bcpp_household.models import Plot
from apps.bcpp_survey.models import Survey
from collections import OrderedDict
from datetime import datetime, date
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.device.device.classes import device
from edc.lab.lab_packing.models import DestinationTuple
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc.map.classes import site_mappers
from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple


try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2013, 10, 18, 0, 0, 0)
study_end_datetime = datetime(2016, 10, 17, 23, 0, 0)


class BcppAppConfiguration(BaseAppConfiguration):

    def prepare(self):
        super(BcppAppConfiguration, self).prepare()
        self.update_or_create_survey()
        self.search_limit_setup()

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': False},
        'appointment':
            {'allowed_iso_weekdays': '1234567',
             'use_same_weekday': True,
             'default_appt_type': 'home',
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
        'device_id': device.device_id}

    holidays_setup = {
        'New Year': date(2014, 1, 01),
        'New Year Holiday': date(2014, 1, 02),
        'Good Fiday': date(2014, 4, 18),
        'Easter Monday': date(2014, 4, 21),
        'Labour Day': date(2014, 5, 01),
        'Ascension Day': date(2014, 5, 29),
        'Sir Seretse Khama Day': date(2014, 7, 01),
        'President\'s Day': date(2014, 7, 17),
        'President\'s Day Holiday': date(2014, 7, 21),
        'Independence Day': date(2014, 9, 30),
        'Botswana Day Holiday': date(2014, 10, 01),
        'Christmas Day': date(2014, 12, 25),
        'Boxing Day': date(2014, 12, 26),
        }

    consent_catalogue_list = [
        {'name': BASELINE_SURVEY_SLUG,
         'content_type_map': 'subjectconsent',
         'consent_type': 'study',
         'version': 1,
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'add_for_app': 'bcpp_subject'},
        {'name': 'bcpp-clinic',
         'content_type_map': 'clinicconsent',
         'consent_type': 'study',
         'version': 1,
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'add_for_app': 'bcpp_clinic'},
        ]

    survey_setup = {
        BASELINE_SURVEY_SLUG:
            {'survey_name': 'BCPP Year 1',
             'survey_slug': BASELINE_SURVEY_SLUG,
             'survey_abbrev': 'Y1',
             'datetime_start': study_start_datetime,
             'datetime_end': datetime(2014, 12, 9, 23, 59, 0)},
        'bcpp-year-2':
            {'survey_name': 'BCPP Year 2',
             'survey_slug': 'bcpp-year-2',
             'survey_abbrev': 'Y2',
             'datetime_start': datetime(2014, 12, 10, 0, 0, 0),
             'datetime_end': datetime(2016, 11, 19, 23, 59, 0)},
        'bcpp-year-3':
            {'survey_name': 'BCPP Year 3',
             'survey_slug': 'bcpp-year-3',
             'survey_abbrev': 'Y3',
             'datetime_start': datetime(2016, 11, 20, 0, 0, 0),
             'datetime_end': datetime(2017, 10, 29, 23, 59, 0)}
    }

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                  PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Clinic Viral Load', 'TEST', 'WB'),
                  PanelTuple('Microtube', 'STORAGE', 'WB'),
                  PanelTuple('ELISA', 'TEST', 'WB'),
                  PanelTuple('Venous (HIV)', 'TEST', 'WB'),
                  ],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16')]}

    lab_setup = {'bcpp': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                           PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('Clinic Viral Load', 'TEST', 'WB'),
                           PanelTuple('Microtube', 'STORAGE', 'WB'),
                           PanelTuple('ELISA', 'TEST', 'WB'),
                           PanelTuple('Venous (HIV)', 'TEST', 'WB'),
                           ],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16')],
                 'profile': [ProfileTuple('Microtube', 'WB'),
                             ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('Clinic Viral Load', 'WB'),
                             ProfileTuple('Genotyping', 'WB'),
                             ProfileTuple('ELISA', 'WB')],
                 'profile_item': [ProfileItemTuple('Microtube', 'PL', 0.3, 1),
                                  ProfileItemTuple('Microtube', 'BC', 0.2, 1),
                                  ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('Clinic Viral Load', 'PL', 1.0, 2),
                                  ProfileItemTuple('Clinic Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('Genotyping', 'PL', 1.0, 4),
                                  ProfileItemTuple('Genotyping', 'BC', 0.5, 2),
                                  ProfileItemTuple('ELISA', 'PL', 1.0, 1),
                                  ProfileItemTuple('ELISA', 'BC', 0.5, 1)]}}

    labeling_setup = {'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', 'localhost', '127.0.0.1', True),
                                        LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', 'bcpplab1', None, False),
                                        LabelPrinterTuple('Zebra_Technologies_ZTC_GX430t', 'localhost', None, False),
                                        LabelPrinterTuple('Zebra_Technologies_ZTC_GX430t', 'bcpplab1', None, False),
                                        LabelPrinterTuple('Zebra_Technologies_QLn320', 'localhost', '127.0.0.1', False)],
                      'client': [ClientTuple(hostname='bcpplab1',
                                             printer_name='Zebra_Technologies_ZTC_GK420t',
                                             cups_hostname='bcpplab1',
                                             ip=None,
                                             aliases=None), ],
                      'zpl_template': [
                          aliquot_label or ZplTemplateTuple(
                              'aliquot_label', (
                                  ('^XA\n'
                                   '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS\n'
                                   '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                                   '^BY^FD${aliquot_identifier}^FS\n'
                                   '^FO300,92^A0N,20,20^FD${aliquot_identifier}^FS\n'
                                   '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                                   '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                                   '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                                   '^XZ')), True),
                          ZplTemplateTuple(
                              'requisition_label', (
                                  ('^XA\n'
                                   '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS\n'
                                   '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                                   '^BY^FD${requisition_identifier}^FS\n'
                                   '^FO300,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                                   '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                                   '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                                   '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                                   '^XZ')), False),
                          ZplTemplateTuple(
                              'referral_label', (
                                  ('^XA\n'
                                   '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}^FS\n'
                                   '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                                   '^BY^FD${subject_identifier}^FS\n'
                                   '^FO300,92^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                                   '^FO300,112^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                                   '^FO300,132^A0N,25,20^FDAPPT: ${referral_appt_datetime}^FS\n'
                                   '^FO300,152^A0N,25,20^FDCLINIC: ${referral_clinic}^FS\n'
                                   '^XZ')), False),
                          ]
                      }

    export_plan_setup = {
        'bcpp_subject.subjectreferral': {
            'app_label': 'bcpp_subject',
            'object_name': 'subjectreferral',
            'fields': [],
            'extra_fields': OrderedDict(
                {'plot_identifier': ('subject_visit__household_member__household_structure__'
                                     'household__plot__plot_identifier'),
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
                'scheduled_appt_date',
                'revision',
                'subject_visit',
                'user_created',
                'user_modified'],
            'header': True,
            'track_history': True,
            'show_all_fields': True,
            'delimiter': '|',
            'encrypt': False,
            'strip': True,
            'target_path': '~/export_to_cdc',
            'notification_plan_name': 'referral_file_to_cdc',
        },
        'bcpp_subject.subjectlocator': {
            'app_label': 'bcpp_subject',
            'object_name': 'subjectlocator',
            'fields': [],
            'extra_fields': OrderedDict(
                {'plot_identifier': ('subject_visit__household_member__household_structure__'
                                     'household__plot__plot_identifier'),
                 'dob': 'subject_visit__appointment__registered_subject__dob',
                 'first_name': 'subject_visit__appointment__registered_subject__first_name',
                 'identity': 'subject_visit__appointment__registered_subject__identity',
                 'identity_type': 'subject_visit__appointment__registered_subject__identity_type',
                 'initials': 'subject_visit__appointment__registered_subject__initials',
                 'last_name': 'subject_visit__appointment__registered_subject__last_name',
                 'subject_identifier': 'subject_visit__appointment__registered_subject__subject_identifier',
                 }),
            'exclude': [
                'exported',
                'created',
                'hostname_created',
                'hostname_modified',
                'modified',
                'revision',
                'subject_visit',
                'user_created',
                'user_modified',
                'registered_subject'],
            'header': True,
            'track_history': True,
            'show_all_fields': True,
            'delimiter': '|',
            'encrypt': False,
            'strip': True,
            'target_path': '~/export_to_cdc',
            'notification_plan_name': 'locator_file_to_cdc',
        }
    }

    notification_plan_setup = {
        'referral_file_to_cdc': {
            'name': 'referral_file_to_cdc',
            'friendly_name': 'BCPP Participant Referral File Transfer to Clinic',
            'subject_format': '{exit_status}: ' + 'BCPP Site {0}'.format(settings.SITE_CODE) + ' Referral File Transfer {timestamp}',
            'body_format': ('Dear BCPP File Transfer Monitoring Group Member,\n\nYou are receiving this email as a member '
                            'of the BCPP file transfer monitoring group. If you have any questions or comments regarding the contents '
                            'of this message please direct them to Erik van Widenfelt (ew2789@gmail.com).\n\n'
                            'To unsubscribe, please contact Erik van Widenfelt (ew2789@gmail.com).\n\n'
                            'File transfer status for {export_datetime} is as follows:\n\n') + (
                                '* Site: {0}: {1}\n'.format(settings.SITE_CODE, settings.CURRENT_COMMUNITY)) + (
                                    '* Transfer Title: {notification_plan_name}\n'
                                    '* Status: {exit_status}\n'
                                    '* Status Message: {exit_status_message}\n'
                                    '* Transaction count: {tx_count}\n'
                                    '* File name: {file_name}\n\n'
                                    'Thank You,\n\n'
                                    'BHP Data Management Team\n'),
            'recipient_list': ['ew2789@gmail.com', 'bcpp-mon@lists.bhp.org.bw'],
            'cc_list': [],
        },
        'locator_file_to_cdc': {
            'name': 'locator_file_to_cdc',
            'friendly_name': 'BCPP Participant Locator File Transfer to Clinic',
            'subject_format': '{exit_status}: ' + 'BCPP Site {0}'.format(settings.SITE_CODE) + ' Locator File Transfer {timestamp}',
            'body_format': ('Dear BCPP File Transfer Monitoring Group Member,\n\nYou are receiving this email as a member '
                            'of the BCPP file transfer monitoring group. If you have any questions or comments regarding the contents '
                            'of this message please direct them to Erik van Widenfelt (ew2789@gmail.com).\n\n'
                            'To unsubscribe, please contact Erik van Widenfelt (ew2789@gmail.com).\n\n'
                            'File transfer status for {export_datetime} is as follows:\n\n') + (
                                '* Site: {0}: {1}\n'.format(settings.SITE_CODE, settings.CURRENT_COMMUNITY)) + (
                                '* Transfer Title: {notification_plan_name}\n'
                                '* Status: {exit_status}\n'
                                '* Status Message: {exit_status_message}\n'
                                '* Transaction count: {tx_count}\n'
                                '* File name: {file_name}\n\n'
                                'Thank You,\n\n'
                                'BHP Data Management Team\n'),
            'recipient_list': ['ew2789@gmail.com', 'bcpp-mon@lists.bhp.org.bw'],
            'cc_list': [],
        }
    }

    @property
    def study_site_setup(self):
        """Returns a dictionary of the the site code and site name.

        Plot checks are bypassed if:
            * CURRENT_COMMUNITY == 'BHP'
            * SITE_CODE=='00'
            * DEVICE_ID in ['99', ]

        Confirms:
            * mapper name an code match that in settings.
            * plot identifier community prefix is the same as the site code.
        """
        try:
            map_code = site_mappers.get_current_mapper().map_code
        except AttributeError:
            map_code = '00'
        if map_code != settings.SITE_CODE:
            raise ImproperlyConfigured('Community code \'{}\' returned by mapper does not equal '
                                       'settings.SITE_CODE \'{}\'.'.format(map_code, settings.SITE_CODE))
        try:
            map_area = site_mappers.get_current_mapper().map_area
        except AttributeError:
            map_area = 'BHP'
        if map_area != settings.CURRENT_COMMUNITY:
            raise ImproperlyConfigured('Current community {} returned by mapper does not equal '
                                       'settings.CURRENT_COMMUNITY {}.'.format(map_area, settings.CURRENT_COMMUNITY))
        try:
            community_check = settings.CURRENT_COMMUNITY_CHECK
        except AttributeError:
            community_check = True
        if str(device) not in ['99', ] and community_check:
            try:
                if Plot.objects.all()[0].plot_identifier[:2] != map_code:
                    raise ImproperlyConfigured('Community code {2} does not correspond with community code segment '
                                               'in Plot identifier {0}. Got {1} != {2}'.format(
                                                   Plot.objects.all()[0].plot_identifier,
                                                   Plot.objects.all()[0].plot_identifier[:2],
                                                   map_code))
            except IndexError:
                pass
        return {'site_name': map_area,
                'site_code': map_code}

    def update_or_create_survey(self):
        for survey_values in self.survey_setup.itervalues():
            try:
                survey = Survey.objects.get(survey_name=survey_values.get('survey_name'))
                survey.survey_slug = survey_values.get('survey_slug')
                survey.survey_abbrev = survey_values.get('survey_abbrev')
                survey.datetime_start = survey_values.get('datetime_start')
                survey.datetime_end = survey_values.get('datetime_end')
                survey.save()
            except Survey.DoesNotExist:
                Survey.objects.create(**survey_values)

    def search_limit_setup(self):
        if not str(device) == '99':
            if not (settings.LIMIT_EDIT_TO_CURRENT_SURVEY and settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY and settings.FILTERED_DEFAULT_SEARCH):
                raise ImproperlyConfigured('LIMIT_EDIT_TO_CURRENT_SURVEY,  LIMIT_EDIT_TO_CURRENT_COMMUNITY and FILTERED_DEFAULT_SEARCH'
                ' should be set to true in a notebook. Update in bcpp_settings.py.'
                )
        elif str(device) == '99':
            if (settings.LIMIT_EDIT_TO_CURRENT_SURVEY and settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY and settings.FILTERED_DEFAULT_SEARCH):
                raise ImproperlyConfigured('LIMIT_EDIT_TO_CURRENT_SURVEY,  LIMIT_EDIT_TO_CURRENT_COMMUNITY and FILTERED_DEFAULT_SEARCH'
                ' should be set to false in a central server. Update in bcpp_settings.py.'
                )

bcpp_app_configuration = BcppAppConfiguration()
