MY_INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',   # DONT TOUCH!!
    'django_databrowse',
    'dajaxice',
    'storages',
    'dajax',
    #'south',

    'edc.apps.admin_supplemental_fields',
    'edc.apps.app_configuration',

    #'edc.base.admin',
    'edc.base.form',
    'edc.base.model',

    'edc.core.identifier',
    'edc.core.crypto_fields',
    'edc.core.model_data_inspector',
    'edc.core.model_selector',
    'edc.core.bhp_templates',
    'edc.core.bhp_static',
    'edc.core.bhp_string',
    'edc.core.bhp_userprofile',
    'edc.core.bhp_poll_mysql',
    'edc.core.bhp_templatetags',
    'edc.core.bhp_common',
    'edc.core.bhp_content_type_map',
    'edc.core.bhp_data_manager',
    'edc.core.bhp_variables',
    'edc.core.bhp_site_edc',
    'edc.core.bhp_nmap',
    'edc.core.bhp_context',
    'edc.core.bhp_using',
    'edc.core.bhp_export_data',
    'edc.core.bhp_birt_reports',

    'edc.device.inspector',
    'edc.device.dispatch',
    'edc.device.netbook',
    'edc.device.device',
    'edc.device.sync',

    'edc.dashboard.base',
    'edc.dashboard.search',
    'edc.dashboard.subject',
    'edc.dashboard.section',

    'edc.export',
    'edc.import',
    'edc.entry_meta_data',

    'edc.data_dictionary',

    'edc.map',

    'edc.testing',
    'edc.utils',

    'edc.subject.lab_tracker',
    'edc.subject.code_lists',
    'edc.subject.rule_groups',
    'edc.subject.actg',
    'edc.subject.entry',
    'edc.subject.consent',
    'edc.subject.contact',
    'edc.subject.locator',
    'edc.subject.subject_summary',
    'edc.subject.off_study',
    'edc.subject.registration',
    'edc.subject.appointment',
    'edc.subject.appointment_helper',
    'edc.subject.visit_schedule',
    'edc.subject.visit_tracking',
    'edc.subject.appointment',
    'edc.subject.subject',
    'edc.subject.subject_config',
    'edc.subject.adverse_event',

    'edc.notification',

    'edc.lab.lab_clinic_api',
    'edc.lab.lab_clinic_reference',
    'edc.lab.lab_requisition',
    'edc.lab.lab_packing',
    'edc.lab.lab_profile',

    'lis.base.model',
    'lis.labeling',
    'lis.core.lab_common',
    'lis.core.lab_flag',
    'lis.core.lab_reference',
    'lis.core.lab_grading',

    'lis.core.lab_result_report',
    'lis.core.bhp_research_protocol',
    'lis.core.lock',

    'lis.specimen.lab_aliquot_list',
    'lis.specimen.lab_panel',
    'lis.specimen.lab_test_code',
    'lis.specimen.lab_receive',
    'lis.specimen.lab_aliquot',
    'lis.specimen.lab_order',
    'lis.specimen.lab_result',
    'lis.specimen.lab_result_item',

    'lis.subject.lab_account',
    'lis.subject.lab_patient',

    'lis.exim.lab_export',
    'lis.exim.lab_import',
    'lis.exim.lab_import_lis',
    'lis.exim.lab_import_dmis',

    'apps.bcpp',
    'apps.bcpp.app_configuration',
    'apps.bcpp_list',
    'apps.bcpp_dashboard',
    'apps.bcpp_stats',
    'apps.bcpp_household',
    'apps.bcpp_subject',
    'apps.bcpp_household_member',
    'apps.bcpp_lab',
    'apps.bcpp_survey',
    'apps.bcpp_inspector',
    'apps.bcpp_dispatch',
    'apps.bcpp_analytics',
    'apps.bcpp_administration',
    'tastypie',
    'edc.audit',
)
