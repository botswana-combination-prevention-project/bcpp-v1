from datetime import datetime
#from django.db.models import get_model

# from edc.core.bhp_content_type_map.models import ContentTypeMap
#from collections import OrderedDict
#from django.conf import settings
from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

#from apps.bcpp_survey.models import Survey

study_start_datetime = datetime(2013, 10, 18, 10, 30, 00)
study_end_datetime = datetime(2014, 10, 17, 16, 30, 00)


class BcppClinicConfiguration(BaseAppConfiguration):

    def prepare(self):
        super(BcppClinicConfiguration, self).prepare()

    global_configuration = {'dashboard': {'show_not_required_metadata': False, 'allow_additional_requisitions': False, 'show_drop_down_requisitions': False},
                            'appointment': {'allowed_iso_weekdays': '12345', 'use_same_weekday': True, 'default_appt_type': 'default'},
                                 }

    study_variables_setup = {
                'protocol_number': 'BHP066',
                'protocol_code': '066',
                'protocol_title': 'BCPP Clinic',
                'research_title': 'Botswana Combination Prevention Project - CLINIC',
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
                'content_type_map': 'clinicconsent',
                'consent_type': 'sub-study',
                'version': 1,
                'start_datetime': datetime(2013, 12, 16, 10, 30, 00),
                'end_datetime': datetime(2014, 12, 23, 16, 30, 00),
                'add_for_app': 'bcpp_clinic'}

    study_site_setup = [{'site_name': 'Digawana', 'site_code': '12'},
                        {'site_name': 'Otse', 'site_code': '14'},
                        {'site_name': 'Lentsweletau', 'site_code': '16'},
                        {'site_name': 'Oodi', 'site_code': '18'},
                        {'site_name': 'Mmankgodi', 'site_code': '20'},
                        ]

    lab_clinic_api_setup = {
          'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                    PanelTuple('Viral Load', 'TEST', 'WB'), ],
          'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                           AliquotTypeTuple('Plasma', 'PL', '32'),
                           AliquotTypeTuple('Buffy Coat', 'BC', '16')],
                          }

    lab_setup = {'clinic': {
                       'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB'),
                                 PanelTuple('Viral Load', 'TEST', 'WB'),
                                ],
                      'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                       AliquotTypeTuple('Plasma', 'PL', '32'),
                                       AliquotTypeTuple('Buffy Coat', 'BC', '16')],
                      'profile': [ProfileTuple('Viral Load', 'WB'),
                                  ProfileTuple('Research Blood Draw', 'WB')],
                      'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 2),
                                       ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                       ProfileItemTuple('Research Blood Draw', 'PL', 1.0, 4),
                                       ProfileItemTuple('Research Blood Draw', 'BC', 0.5, 2)]}}

    labeling_setup = {'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', 'silverapple', '127.0.0.1', True)],
                      'client': [ClientTuple(hostname='silverapple',
                                             aliases=None,
                                             ip=None,
                                             printer_name='Zebra_Technologies_ZTC_GK420t',
                                             cups_hostname='silverapple',
                                             ), ],
                      'zpl_template': [
                     ZplTemplateTuple(
                         'aliquot_label', (
                             """^XA
                             ^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS
                             ^FO300,34^BY1,3.0^BCN,50,N,N,N
                             ^BY^FD${aliquot_identifier}^FS
                             ^FO300,92^A0N,20,20^FD${aliquot_identifier}^FS
                             ^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS
                             ^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS
                             ^FO300,152^A0N,25,20^FD${drawn_datetime}^FS
                             ^XZ"""
                             ),
                         True)],
                 }

    consent_catalogue_list = [consent_catalogue_setup]

    def update_or_create_study_variables(self):
        if StudySpecific.objects.all().count() == 0:
            StudySpecific.objects.create(**self.study_variables_setup)
        else:
            StudySpecific.objects.all().update(**self.study_variables_setup)
        self._setup_study_sites()

    def _setup_study_sites(self):
        for site in self.study_site_setup:
            try:
                StudySite.objects.get(**site)
            except StudySite.DoesNotExist:
                StudySite.objects.create(**site)
