from fabric.api import local, run, cd, put, env, get
import tempfile
from shutil import move
import os


repo_url = '192.168.1.50/svn'
settings_file = 'settings.py'
remote_proj_dir = '/Users/django/source/bhp066'
host_ids = ['82', '138', '230', '112', '120', '127', '21', '205', '170',
            '187', '244']
ips = ['192.168.1.' + id for id in host_ids]
net_id = ['92', '90', '60', '42', '83', '10', '54', '70', '78', '12', '15']
ip_id = dict(zip(ips, net_id))
ip_id = {'192.168.1.112': '42'}
#env.hosts = ips


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
        local("svn co %s/%s" % (repo_url, repo,))
        print "finished checking out '%s'" % repo

    print "and we are done checking out projects! woohoo!"


def provision():
    print "executing provisioning for %s" % env.host

    with cd(remote_proj_dir):
        svn_update('bcpp*')
        svn_update('bhp*')
        svn_update('lab*')
        svn_update(settings_file)
        svn_update('url.py')
        svn_checkout('bcpp_inspector')
        svn_checkout('bhp_inspector')
        syncdb()
        modify_remote_settings(_uncomment_south)
        syncdb()
        fake_migrate()
        svn_update(settings_file)

    modify_remote_settings(_deviceid_and_keypath)
    print "finished provisioning!! Yep!"


def svn_checkout(repo):
    print "checking out a repository '%s'" % repo
    run('svn co http://192.168.1.50/svn/%s' % repo)


def svn_update(item):
    print "svn updating of '%s'" % item
    run('svn update %s' % item)


def syncdb():
    print "syncdb started ..."
    run('python manage.py syncdb')


def fake_migrate():
    print "fake migration started.."
    run('python manage.py migrate --fake')


def clean_pyc():
    print "clean_pyc started"
    run('python manage clean_pyc')


def modify_remote_settings(func):
    tmp_dir = tempfile.mkdtemp()
    get(_path_of(remote_proj_dir, settings_file), tmp_dir)
    file_to_modify = _path_of(tmp_dir, settings_file)
    modified_file = process_line(file_to_modify, func)
    put(modified_file, remote_proj_dir)


def uncomment_south():
    tmp_dir = tempfile.mkdtemp()
    get(_path_of(remote_proj_dir, settings_file), tmp_dir)
    file_to_modify = _path_of(tmp_dir, settings_file)
    modified_file = process_line(file_to_modify, _uncomment_south)
    put(modified_file, remote_proj_dir)


def _uncomment_south(new_file, line):
    trimmed_line = line.replace(" ", '')
    if trimmed_line.startswith("#'south'"):
        new_file.write("\t'south',\n")
    else:
        new_file.write(line)


def _deviceid_and_keypath(new_file, line):
    dev_id = ip_id.get(env.host)
    trimmed_line = line.replace(' ', '')
    if trimmed_line.startswith('#'):
        new_file.write(line)
        return

    if "KEY_PATH=" in trimmed_line:
        new_file.write("KEY_PATH = '/Volumes/keys'\n")
    elif "DEVICE_ID=" in trimmed_line:
        new_file.write("DEVICE_ID = '%s' \n" % dev_id)
    else:
        new_file.write(line)


def process_line(file_path, func):
    fh, abs_path = tempfile.mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path)
    for line in old_file:
        func(new_file, line)
    new_file.close()
    os.close(fh)
    old_file.close()
    os.remove(file_path)
    move(abs_path, file_path)
    return file_path


def _path_of(dir, file):
    return os.path.join(dir, file)
