from fabric.api import local, run, cd, put


def checkout_repo():
    repos = ('audit_trail', 'autocomplete', 'bhp_templates', 'bhp_static',
             'bhp_crypto', 'bhp_string', 'bhp_lock', 'bhp_appointment_helper',
             'bhp_userprofile', 'bhp_poll_mysql', 'bhp_model_selector',
             'bhp_templatetags', 'bhp_calendar', 'bhp_base_model',
             'bhp_base_test', 'bhp_variables', 'bhp_actg_reference',
             'bhp_adverse', 'bhp_map', 'bhp_code_lists', 'bhp_common',
             'bhp_identifier', 'bhp_content_type_map', 'bhp_search',
             'bhp_section', 'bhp_consent', 'bhp_locator', 'bhp_off_study',
             'bhp_registration', 'bhp_botswana', 'bhp_data_manager',
             'bhp_base_admin', 'bhp_base_form', 'bhp_supplemental_fields',
             'bhp_variables', 'bhp_site_edc', 'bhp_research_protocol',
             'bhp_sync', 'bhp_device', 'lab_common', 'lab_import',
             'lab_import_lis', 'lab_import_dmis', 'lab_flag', 'lab_grading',
             'lab_reference', 'lab_requisition', 'lab_aliquot_list',
             'lab_base_model', 'lab_panel', 'lab_test_code', 'lab_account',
             'lab_patient', 'lab_receive', 'lab_aliquot', 'lab_order',
             'lab_result', 'lab_result_item', 'lab_barcode', 'lab_clinic_api',
             'lab_clinic_reference', 'lab_export', 'lab_result_report',
             'lab_packing', 'lab_base_model', 'bhp_lab_tracker', 'bhp_visit',
             'bhp_visit_tracking', 'bhp_appointment', 'bhp_subject',
             'bhp_subject_config', 'bhp_supplemental_fields', 'bhp_nmap',
             'bhp_data_manager', 'bhp_entry', 'bhp_lab_entry', 'bhp_context',
             'bhp_birt_reports', 'bhp_using', 'bhp_contact', 'bhp_dashboard',
             'bhp_dashboard_registered_subject', 'bhp_export_data',
             'bhp_model_describer', 'bhp_subject_summary', 'bhp_entry_rules',
             'bhp_dispatch', 'bhp_netbook', 'bhp_household',
             'bhp_household_member', 'bcpp', 'bcpp_lab', 'bcpp_list',
             'bcpp_subject', 'bcpp_dashboard', 'bcpp_stats', 'bcpp_household',
             'bcpp_household_member', 'bcpp_survey',)

    print "total number of repos = %d" % len(repos)

    for repo in repos:
        print "SVN checkout of '%s' ...." % repo
        local("svn co http://192.168.1.50/svn/%s" % repo)
        print "finished checking out '%s'" % repo

    print "and we are done checking out projects! woohoo!"


def syncdb():
    run('python manage.py syncdb')


def fake_migrate():
    run('python manage.py migrate --fake')


def clean_pyc():
    run('python manage clean_pyc')


def uncomment_south():
    put('settings_south_on.py, settings.py')


def svn_checkout(repo):
    run('svn co http://192.168.1.50/svn/%s' % repo)


def svn_update(item):
    run('svn update %s' % item)


def provision():
    src_dir = '/Users/django/source/bhp066'
    with cd(src_dir):
        svn_update('bcpp*')
        svn_update('bhp*')
        svn_update('lab*')
        svn_checkout('bcpp_inspector')
        svn_checkout('bhp_inspector')
        syncdb()
        uncomment_south()
        syncdb()
        fake_migrate()
        svn_update('settings.py')
