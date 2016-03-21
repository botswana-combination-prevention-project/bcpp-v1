import socket

from collections import OrderedDict
from datetime import datetime, date, timedelta

from django.conf import settings

from bhp066.apps.bcpp_household.constants import BASELINE_SURVEY_SLUG
from bhp066.apps.bcpp_household.models import Plot

from django.core.exceptions import ImproperlyConfigured

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc_device import device
from edc.lab.lab_packing.models import DestinationTuple
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc.map.classes import site_mappers
from edc_consent.models import ConsentType

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from bhp066.apps.bcpp_survey.models import Survey

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
        self.prep_survey_for_tests()
        self.search_limit_setup()
        self.update_or_create_consent_type()

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
        'New Year': date(2016, 1, 1),
        'New Year Holiday': date(2016, 1, 2),
        'Good Fiday': date(2016, 3, 25),
        'Easter Monday': date(2016, 3, 28),
        'Labour Day': date(2016, 5, 2),
        'Ascension Day': date(2016, 5, 5),
        'Sir Seretse Khama Day': date(2016, 7, 1),
        'President\'s Day': date(2016, 7, 18),
        'President\'s Day Holiday': date(2016, 7, 19),
        'Independence Day': date(2016, 9, 30),
        'Botswana Day Holiday': date(2016, 10, 1),
        'Christmas Day': date(2016, 12, 25),
        'Christmas Holiday': date(2016, 12, 27),
        'Boxing Day': date(2016, 12, 26),
    }

    survey_setup = {
        BASELINE_SURVEY_SLUG:
            {'survey_name': 'BCPP Year 1',
             'survey_slug': BASELINE_SURVEY_SLUG,
             'survey_abbrev': 'Y1',
             'datetime_start': study_start_datetime,
             'datetime_end': datetime(2016, 2, 30, 23, 59, 0),
             'chronological_order': 1},
        'bcpp-year-2':
            {'survey_name': 'BCPP Year 2',
             'survey_slug': 'bcpp-year-2',
             'survey_abbrev': 'Y2',
             'datetime_start': datetime(2016, 3, 12, 0, 0, 0),
             'datetime_end': datetime(2016, 5, 30, 23, 59, 0),
             'chronological_order': 2},
        'bcpp-year-3':
            {'survey_name': 'BCPP Year 3',
             'survey_slug': 'bcpp-year-3',
             'survey_abbrev': 'Y3',
             'datetime_start': datetime(2016, 12, 1, 0, 0, 0),
             'datetime_end': datetime(2017, 10, 29, 23, 59, 0),
             'chronological_order': 3},
    }

    consent_type_setup = [
        {
            'app_label': 'bcpp_subject',
            'model_name': 'subjectconsent',
            'start_datetime': datetime(2015, 9, 16, 0, 0, 0),
            'end_datetime': datetime(2017, 12, 31, 23, 59, 0),
            'version': '4',
        },
        {
            'app_label': 'bcpp_clinic',
            'model_name': 'clinicconsent',
            'start_datetime': datetime(2013, 10, 18, 0, 0, 0),
            'end_datetime': datetime(2016, 10, 17, 23, 0, 0),
            'version': '1',
        },
        {
            'app_label': 'bcpp_subject',
            'model_name': 'subjectconsentextended',
            'start_datetime': datetime(2015, 9, 16, 0, 0, 0),
            'end_datetime': datetime(2017, 12, 31, 23, 59, 0),
            'version': '4',
        },
        {
            'app_label': 'bcpp_subject',
            'model_name': 'subjectconsent',
            'start_datetime': datetime(2015, 5, 1, 0, 0, 0),
            'end_datetime': datetime(2015, 9, 15, 23, 59, 0),
            'version': '3',
        },
        {
            'app_label': 'bcpp_subject',
            'model_name': 'subjectconsent',
            'start_datetime': datetime(2014, 4, 10, 0, 0, 0),
            'end_datetime': datetime(2015, 4, 30, 23, 59, 0),
            'version': '2',
        },
        {
            'app_label': 'bcpp_subject',
            'model_name': 'subjectconsent',
            'start_datetime': datetime(2013, 10, 30, 0, 0, 0),
            'end_datetime': datetime(2014, 4, 9, 23, 59, 0),
            'version': '1',
        },
    ]

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                  PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Viral Load (Abbott)', 'TEST', 'WB'),
                  PanelTuple('Viral Load (POC)', 'TEST', 'WB'),
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
                           PanelTuple('Viral Load (Abbott)', 'TEST', 'WB'),
                           PanelTuple('Viral Load (POC)', 'TEST', 'WB'),
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

    labeling_setup = {
        'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', 'localhost', '127.0.0.1', True),
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
                     '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} '
                     '${aliquot_count}${primary}^FS\n'
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
                     '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} '
                     '${aliquot_count}${primary}^FS\n'
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
                     '^XZ')), False)]
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
                'user_modified',
                'consent_version'],
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
                'registered_subject',
                'consent_version'],
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
            'subject_format': '{exit_status}: ' + 'BCPP Site {0}'.format(settings.SITE_CODE) + ' Referral File Transfer'
            ' {timestamp}',
            'body_format': ('Dear BCPP File Transfer Monitoring Group Member,\n\nYou are receiving this email as a '
                            'member '
                            'of the BCPP file transfer monitoring group. If you have any questions or comments '
                            'regarding the contents '
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
            'subject_format': '{exit_status}: ' + 'BCPP Site {0}'.format(settings.SITE_CODE) + ' Locator File '
            'Transfer {timestamp}',
            'body_format': ('Dear BCPP File Transfer Monitoring Group Member,\n\nYou are receiving this email as a '
                            'member '
                            'of the BCPP file transfer monitoring group. If you have any questions or comments '
                            'regarding the contents '
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

    quota_client_setup = [
        'bcpp001', 'bcpp005', 'bcpp007', 'bcpp008', 'bcpp009', 'bcpp010', 'bcpp011', 'bcpp012', 'bcpp014',
        'bcpp015', 'bcpp016', 'bcpp018', 'bcpp019', 'bcpp022', 'bcpp023', 'bcpp024', 'bcpp025', 'bcpp027',
        'bcpp028', 'bcpp030', 'bcpp031', 'bcpp034', 'bcpp035', 'bcpp037', 'bcpp038', 'bcpp039', 'bcpp040',
        'bcpp043', 'bcpp048', 'bcpp049', 'bcpp050', 'bcpp051', 'bcpp052', 'bcpp053', 'bcpp054', 'bcpp055',
        'bcpp056', 'bcpp062', 'bcpp063', 'bcpp064', 'bcpp065'
    ]

    @property
    def study_site_setup(self):
        """Returns a dictionary of the the site code and site name.

        Plot checks are bypassed if:
            * CURRENT_COMMUNITY == 'BHP'
            * SITE_CODE=='00'
            * DEVICE_ID in [device.central_server_id, ]

        Confirms:
            * mapper name an code match that in settings.
            * plot identifier community prefix is the same as the site code.
        """
        try:
            map_code = site_mappers.get_mapper(site_mappers.current_community).map_code
        except AttributeError:
            map_code = '00'
        if self.confirm_site_code_in_settings:  # default is True, set to False for tests
            if map_code != settings.SITE_CODE:
                raise ImproperlyConfigured('Community code \'{}\' returned by mapper does not equal '
                                           'settings.SITE_CODE \'{}\'.'.format(map_code, settings.SITE_CODE))
        try:
            map_area = site_mappers.get_mapper(site_mappers.current_community).map_area
        except AttributeError:
            map_area = 'BHP'
        if self.confirm_community_in_settings:  # default is True, set to False for tests
            if map_area != settings.CURRENT_COMMUNITY:
                raise ImproperlyConfigured(
                    'Current community {} returned by mapper does not equal '
                    'settings.CURRENT_COMMUNITY {}.'.format(map_area, settings.CURRENT_COMMUNITY))
        return self.validate_plot(map_area, map_code)

    def validate_plot(self, map_area, map_code):
        try:
            community_check = settings.CURRENT_COMMUNITY_CHECK
        except AttributeError:
            community_check = True
        if str(device) not in [device.central_server_id, ] and community_check:
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
                survey.chronological_order = survey_values.get('chronological_order')
                survey.save()
            except Survey.DoesNotExist:
                Survey.objects.create(**survey_values)

    def update_or_create_consent_type(self):
        for item in self.consent_type_setup:
            try:
                consent_type = ConsentType.objects.get(
                    version=item.get('version'),
                    app_label=item.get('app_label'),
                    model_name=item.get('model_name'))
                consent_type.start_datetime = item.get('start_datetime')
                consent_type.end_datetime = item.get('end_datetime')
                consent_type.save()
            except ConsentType.DoesNotExist:
                ConsentType.objects.create(**item)

    def search_limit_setup(self):
        if str(device) == device.central_server_id:
            if (settings.LIMIT_EDIT_TO_CURRENT_SURVEY and
                    settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY and
                    settings.FILTERED_DEFAULT_SEARCH):
                raise ImproperlyConfigured(
                    'LIMIT_EDIT_TO_CURRENT_SURVEY,  LIMIT_EDIT_TO_CURRENT_COMMUNITY '
                    'and FILTERED_DEFAULT_SEARCH should be set to false in a central '
                    'server. Update in bcpp_settings.py.')
        else:
            if not (settings.LIMIT_EDIT_TO_CURRENT_SURVEY and
                    settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY and
                    settings.FILTERED_DEFAULT_SEARCH):
                raise ImproperlyConfigured(
                    'LIMIT_EDIT_TO_CURRENT_SURVEY,  LIMIT_EDIT_TO_CURRENT_COMMUNITY '
                    'and FILTERED_DEFAULT_SEARCH should be set to true in a notebook. '
                    'Update in bcpp_settings.py.')

    @property
    def survey_dates(self):
        survey_dates = []
        start_date = datetime.today() - timedelta(days=1)
        end_date = datetime.today() + timedelta(days=30)
        full_enrollment_date = end_date
        for _ in range(3):
            survey_dates.append((start_date, end_date, full_enrollment_date))
            start_date = end_date + timedelta(days=2)
            end_date = start_date + timedelta(days=30)
            full_enrollment_date = end_date
        return survey_dates

    def update_survey(self, survey, survey_dates):
        survey.datetime_start, survey.datetime_end, full_enrollment_date = survey_dates
        full_enrollment_date = full_enrollment_date
        survey.save()

    def prep_survey_for_tests(self):
        surveys = Survey.objects.all()
        mapper = site_mappers.get_mapper(site_mappers.current_community)
        if socket.gethostname() in settings.ADMINS_HOST:
            survey_slug = [(1, 2, 3), (2, 1, 3), (3, 1, 2)][int(settings.CURRENT_SURVEY[-1]) - 1]
            for j, survey_dates in enumerate(self.survey_dates):
                survey_year = 'bcpp-year-{}'.format(survey_slug[j])
                survey = surveys.filter(survey_slug=survey_year).first()
                self.update_survey(survey, survey_dates)
                self.update_site_mapper(mapper, survey_year, survey_dates)

    def update_site_mapper(self, mapper, survey_year, survey_dates):
        from collections import namedtuple
        SurveyDatesTuple = namedtuple(
            'SurveyDatesTuple', 'name start_date full_enrollment_date end_date smc_start_date')
        start_date, end_date, full_enrollment_date = survey_dates
        start_date = start_date + timedelta(days=1)
        survey_date = SurveyDatesTuple(
            name='t{}'.format(survey_year[-1]),
            start_date=start_date.date(),
            full_enrollment_date=full_enrollment_date.date(),
            end_date=end_date.date(),
            smc_start_date=datetime.today().date())
        mapper.survey_dates[survey_year] = survey_date
        return mapper

bcpp_app_configuration = BcppAppConfiguration()
