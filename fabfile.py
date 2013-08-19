from fabric.api import local, run, cd, put, env, get
import tempfile
from shutil import move
import os


env.svn_repo = '192.168.1.50/svn'
env.netbook_proj_dir = '/Users/django/source/bhp066'


def setup_vagrant_as_host():
    env.user = 'vagrant'
    env.hosts = ['192.168.16.8']
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]


def set_netbooks_as_hosts():
    host_ids = ['82', '138', '230', '112', '120', '127', '21', '205', '170', '187', '244']
    ips = ['192.168.1.' + id for id in host_ids]
    netbook_id = ['92', '90', '60', '42', '83', '10', '54', '70', '78', '12', '15']
    env.netbook_ip_id = dict(zip(ips, netbook_id))
    env.hosts = ips


def checkout_app_repos():
    installed_apps = get_setting().INSTALLED_APPS
    repos = filter(RepoFilter(['au', 'bcpp', 'bhp', 'lab']), installed_apps)
    print "total number of repos = %d" % len(repos)
    for repo in repos:
        local("svn co %s/%s" % (env.svn_repo, repo,))
    print "and we are done checking out projects! woohoo!"


def get_setting(key=None):
    try:
        settings = __import__("settings", globals(), locals(), [], 0)
        if not key:
            return settings
        try:
            return settings[key]
        except KeyError:
            print "Key: %s not found" % key
            raise ImportError
    except ImportError:
        print "Error encountered reading the settings file"
        exit()


class RepoFilter(object):
    def __init__(self, prefixes):
        self.prefixes = prefixes

    def __call__(self, repo):
        for prefix in self.prefixes:
            if repo.startswith(prefix):
                return True
        return False


settings_file = 'settings.py'
ip_id_map = {'192.168.1.112': '42'}
#env.hosts = ips
#env.hosts = ['django@192.168.1.112']
#env.password = 'aM+u*Z0O'


def drop_db():
    run('drop database bhp066_survey')


def create_db():
    run('create database bhp066_survey')


def provision():
    """ The main task for provisioning netbook """
    print "executing provisioning for %s" % env.host
    with cd(env.netbook_proj_dir):
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
    run('svn co %s/%s' % (env.svn_repo, repo,))


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
    get(_path_of(env.netbook_proj_dir, settings_file), tmp_dir)
    file_to_modify = _path_of(tmp_dir, settings_file)
    modified_file = process_line(file_to_modify, func)
    put(modified_file, env.netbook_proj_dir)


def _uncomment_south(new_file, line):
    trimmed_line = line.replace(" ", '')
    if trimmed_line.startswith("#'south'"):
        new_file.write("\t'south',\n")
    else:
        new_file.write(line)


def _comment_out_south(new_file, line):
    trimmed_line = line.replace(' ', '')
    if trimmed_line.startswith("'south',"):
        new_file.write(line)
        return
    if "'south'" in trimmed_line:
        new_file.write("\t#'south',\n")
    else:
        new_file.write(line)


def _deviceid_and_keypath(new_file, line):
    dev_id = ip_id_map.get(env.host)
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
