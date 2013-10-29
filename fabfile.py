import os

import time
import datetime

from fabric.api import *
from fabric.contrib.files import exists
from fabric.colors import green, red


#modify host ids to include last number of ips to run script on e.g. host_ids = ['22', '16', '133']
host_ids = ['75']
# '237', '125'

#current branch to checkout. Set it to the current branch you want to checkout. e.g. '121'
env.git_branch = 'master'

#modify to point to the db sql statements file in fabric/sql directory. File must exist!
env.base_sql = 'base_bhp066_db_20131024.sql'

#modify username and host according to host
env.user = 'django'
env.password = 'django'

env.setuptools = 'setuptools-1.1.6'
env.virtualenv = 'virtualenv-1.9.1'
env.pip = 'pip-1.4.1'
env.virtualenvwrapper = 'virtualenvwrapper-4.1.1'

host_ips = ['192.168.1.' + id for id in host_ids]
env.hosts = host_ips
env.dbname = 'bhp066'
env.mysql_root_passwd = 'cc3721b'

a_dir = a_file = "{0}/{1}".format

SRC_DIR = 'source'
PROJECT_ROOT = '~/source/bhp066_project'
PROJECT_DIR = a_dir(PROJECT_ROOT, 'bhp066')
EDC_DIR = a_dir(PROJECT_DIR, 'edc')
LIS_DIR = a_dir(PROJECT_DIR, 'lis')
VIRTUALENV = 'bhp066_env'
VIRTUALENV_HOME = '~/.virtualenvs'
SETTINGS_DIR = a_dir(PROJECT_DIR, 'bhp066')
SETTINGS_FILE = a_file(SETTINGS_DIR, 'settings.py')
FILE_WITH_SOUTH = '%s/settings.py' % SETTINGS_DIR
UNSOUTHED = 'unsouthed'

VIRTUALENVWRAPPER = '/usr/local/bin/virtualenvwrapper.sh'
VIRTUALENV_PATH = a_dir(VIRTUALENV_HOME, VIRTUALENV)
WORKON_VIRTUALENV = 'workon {virtualenv}'.format(virtualenv=VIRTUALENV)
FAB_PIP_CACHE = '~/.pip_fab/cache'
FAB_WORKON_HOME = '~/.virtualenvs_fab'

FAB_DIR = 'fabric'
FAB_KEYS_DIR = a_dir(FAB_DIR, 'keys')
FAB_SQL_DIR = a_dir(FAB_DIR, 'sql')
FAB_AIR_DIR = a_dir(FAB_DIR, 'mac_air')
FAB_APACHE_DIR = a_dir(FAB_DIR, 'apache')

GIT_PULL = 'git pull origin master'
git_clone = 'git clone git@gitserver:{repo}.git'.format
checkout_branch = "git clone git@gitserver:bhp066_project.git -b {branch}".format

TMP_INSTALL_DIR = 'tmp_installs'


@task
def update_code_db():
    execute(clone_code)
    execute(reset_db)


@task
def reset_db():
    execute(drop_db)
    execute(create_db)
    execute(dump_restore)


@task
def add_images():
    map_images = 'map_images.sql'
    put(a_dir(FAB_DIR, 'media'), PROJECT_DIR)
    put(a_file(FAB_SQL_DIR, 'map_images_update.sql'), a_file(PROJECT_ROOT, map_images))
    with cd(PROJECT_ROOT):
        execute_sql_file(map_images)


@task
def deploy_manual_setup():
    execute(check_for_required_programs)
    execute(clone_code)
    rmdir(VIRTUALENV_HOME)
    execute(transfer_pip_cache)
    execute(drop_db)
    execute(create_db)
    execute(dump_restore)
    execute(bootstrap_virtualenv)
    execute(enable_keys)


@task
def deploy_alpha():
    execute(check_for_required_programs)
    install_pip_if_not_installed()
    execute(clone_code)
    rmdir(VIRTUALENV_HOME)
    execute(transfer_pip_cache)
    execute(drop_db)
    execute(create_db)
    execute(dump_restore)
    execute(setup_virtualenv)
    execute(enable_keys)


@task
def setup_basedb():
    execute(prepare_code)
    comment_out_south()
    syncdb(UNSOUTHED)
    uncomment_south()
    syncdb()
    fake_migration()
    execute(prepare_netbook)


@task
def check_for_required_programs():
    exit_if_not_installed('python')
    exit_if_not_installed('git')
    exit_if_not_installed('mysql')
    exit_if_not_installed('swig')
    print(green("Success: Required programs are installed on host: ['%s']" % env.host))


def install_pip_if_not_installed():
    if program_not_installed('pip'):
        sudo('easy_install -U pip')


def checkout_code():
    if project_is_checked_out():
        execute(update_code)
    else:
        execute(clone_code)


@task
def clone_code():
    rmdir(SRC_DIR, contents_only=True)
    rmdir(SRC_DIR)
    mkdir(SRC_DIR)
    chmod('755', SRC_DIR)
    with cd(SRC_DIR):
        run(checkout_branch(branch=env.git_branch))
    with cd(PROJECT_DIR):
        run(git_clone(repo='edc'))
        run(git_clone(repo='lis'))
        run(git_clone(repo='edc_templates') + ' templates')
    execute(set_device_id)


def project_is_checked_out():
    return exists(EDC_DIR) and exists(LIS_DIR)


@task
def update_code():
    with cd(PROJECT_ROOT):
        run("git pull origin v121")
    with cd(EDC_DIR):
        run(GIT_PULL)
    with cd(LIS_DIR):
        run(GIT_PULL)


@task
def local_setup():
    env.hosts = ['localhost']
    env.user = 'twicet'


@task
def setup_virtualenv():
    if not virtualenv_exists():
        execute(install_virtualenv)
        create_virtualenv()
    execute(install_dependencies())


@task
def install_virtualenv():
    pip_install('virtualenv')
    if not exists(VIRTUALENV_HOME):
        mkdir(VIRTUALENV_HOME)
    pip_install('virtualenvwrapper')
    put('air_profile', '.bash_profile')


@task
def bootstrap_virtualenv():
    setup_venv()
    make_venv()


def setup_venv():
    mkdir(TMP_INSTALL_DIR)
    put('./fabric/installs/*', TMP_INSTALL_DIR)
    install_python_package(env.setuptools, TMP_INSTALL_DIR)
    install_python_package(env.pip, TMP_INSTALL_DIR)
    install_python_package(env.virtualenv, TMP_INSTALL_DIR)
    install_virtualenvwrapper(manual=True, dir=TMP_INSTALL_DIR)


@task
def uninstall_manual_installations(basedir=None):
    if not basedir:
        basedir = TMP_INSTALL_DIR
    with cd(basedir):
        for pack in [env.virtualenvwrapper, env.virtualenv, env.pip, env.setuptools]:
            uninstall_package(pack)


def uninstall_package(package_name):
    if exists(package_name):
        with cd(package_name):
            sudo('python setup.py install --record files.txt')
            sudo('cat files.txt | xargs rm -rf')
        return True
    print(red('package "%s" not installed' % package_name))


def provision_virtualenv():
    execute(install_dependencies())


def install_virtualenvwrapper(manual=False, dir=None):
    if manual:
        install_python_package(env.virtualenvwrapper, dir)
    else:
        pip_install('virtualenvwrapper')
    put('air_profile', '.bash_profile')


def install_python_package(package, within_dir):
    prog_name = package.split('-')[0]
    if program_is_installed(prog_name):
        return False
    with cd(within_dir):
        untar(package)
        with cd(package):
            sudo('python setup.py install')
        rm(package + '.tar.gz')


@task
def make_venv():
    create_virtualenv()
    execute(install_dependencies)


def create_virtualenv(env_name='bhp066_env'):
    sudo('mkvirtualenv  %s' % env_name)


@task
def install_dependencies():
    with prefix(WORKON_VIRTUALENV):
        pip_install('-r %s/requirements.txt' % PROJECT_ROOT)


def virtualenv_exists():
    return exists('%s/%s' % (VIRTUALENV_HOME, VIRTUALENV))


@task
def delete_virtualenv():
    sudo('rmvirtualenv %s' % VIRTUALENV)
    #rmdir(VIRTUALENV_PATH)


@task
def delete_base_env():
    rmdir(VIRTUALENV_HOME)


@task
def reset_installs():
    execute(delete_virtualenv)
    execute(drop_db)
    sudo('pip uninstall virtualenvwrapper')
    rmdir(VIRTUALENV_HOME)


def syncdb(settings_file=None):
    execute(manage_py, 'syncdb --noinput', settings_file)


@task
def migrate_db():
    execute(manage_py, 'migrate')


@task
def fake_migrate():
    execute(manage_py, 'migrate dispatch --fake')
    execute(manage_py, 'migrate sync --fake')
    execute(manage_py, 'migrate netbook --fake')
    execute(manage_py, 'migrate consent --fake')


def fake_migration(settings_file=None):
    execute(manage_py, 'migrate --fake', settings_file)


def create_superuser():
    details = dict(password='cc3721b', is_staff=True, is_active=True, is_superuser=True)
    user, created = User.objects.get_or_create(username='username', defaults=details)


def comment_out_south():
    with cd(SETTINGS_DIR):
        sudo("sed \"s/'south'/\#'south'/g\" settings.py >%s.py" % UNSOUTHED)


def uncomment_south():
    with cd(SETTINGS_DIR):
        rm('%.py' % UNSOUTHED)


@task
def set_mysql_passwd():
    sudo('mysqladmin -u root password %s' % env.mysql_root_passwd)


@task
def dump_backup():
    with cd(SRC_DIR):
        sudo('mysqldump -u root -p%s %s > %s' % (env.mysql_root_passwd, env.dbname, 'backup.sql'))


@task
def dump_restore(restore_sql="restore_dump.sql"):
    put(a_file(FAB_SQL_DIR, env.base_sql), '%s/restore_dump.sql' % SRC_DIR)
    with cd(SRC_DIR):
        execute_sql_file(restore_sql)


def execute_sql_file(sql_file):
    sudo('mysql -u root -p%s %s < %s' % (env.mysql_root_passwd, env.dbname, sql_file))


@task
def create_db():
    create_db_sql = "CREATE DATABASE {dbname}".format(dbname=env.dbname)
    mysql_execute(create_db_sql)


@task
def drop_db():
    drop_db_sql = "DROP DATABASE {dbname}".format(dbname=env.dbname)
    mysql_execute(drop_db_sql)


def mysql_execute(cmd):
    credentials = 'mysql -u root --password={password}'.format(password=env.mysql_root_passwd)
    full_command = 'echo "{sql_command}" | {on_mysql}'.format(sql_command=cmd, on_mysql=credentials)
    sudo(full_command)


@task
def manage_py(command=None, config=None):
    with cd(PROJECT_DIR):
        sudo('chmod a+x manage.py')
        if exists(VIRTUALENVWRAPPER):
            with prefix(WORKON_VIRTUALENV):
                _managepy(command, config)
        else:
            with prefix('source %s/%s/bin/activate' % (VIRTUALENV_HOME, VIRTUALENV)):
                _managepy(command, config)


def _managepy(command=None, config=None):
    with settings(warn_only=True):
        if config:
            sudo('./manage.py {command} --settings=bhp066.{config}'.format(command=command, config=config))
        else:
            sudo('./manage.py {command}'.format(command=command))


def mkdir(dirname, as_sudo=True):
    mkdir_cmd = 'mkdir -p {dir}'.format(dir=dirname)
    if as_sudo:
        sudo(mkdir_cmd)
    else:
        run(mkdir_cmd)
    sudo('chown -R Django:staff %s' % dirname)


def rm(filename, force=True):
    if force:
        sudo('rm -f {filename}'.format(filename=filename))
    else:
        sudo('rm {filename}'.format(filename=filename))


def rmdir(dirname, contents_only=False):
    if contents_only:
        sudo('rm -rf {dir}/*'.format(dir=dirname))
    else:
        sudo('rm -rf {dir}'.format(dir=dirname))


def pip_install(package_name, as_sudo=True):
    install_cmd = 'pip install {package}'.format(package=package_name)
    if as_sudo:
        sudo(install_cmd)
    else:
        run(install_cmd)


@task
def transfer_pip_cache():
    rmdir('.pip')
    put('./fabric/pip_cache.tar.gz', 'cache.tar.gz')
    mkdir('.pip/cache')
    sudo('tar -zxvf cache.tar.gz')
    sudo('mv pip_cache/* .pip/cache')
    rmdir('pip_cache')
    rm('cache.tar.gz')


@task
def enable_keys():
    mpp_netbook = 'mpp_netbook'
    prep_netbook = 'prep_netbook'
    mpp_netbook_zip = mpp_netbook + '.zip'
    prep_netbook_zip = prep_netbook + '.zip'
    rm(mpp_netbook_zip)
    rm(prep_netbook_zip)
    rmdir(mpp_netbook)
    rmdir(prep_netbook)
    rmdir('__MACOSX')
    mounted = exists('/Volumes/keys')
    print(green("Are keys mounted?: %s" % mounted))
    put(a_file(FAB_KEYS_DIR, mpp_netbook_zip), mpp_netbook_zip)
    put(a_file(FAB_KEYS_DIR, prep_netbook_zip), prep_netbook_zip)
    unzip(mpp_netbook_zip)
    unzip(prep_netbook_zip)
    sudo('chown -R Django:staff mpp_netbook')
    sudo('chown -R Django:staff prep_netbook')
    chmod('755', 'prep_netbook', dir=True)
    put('./fabric/keys/mount_keys.sh', '~/mount_keys.sh')
    chmod('755', 'mount_keys.sh')
    #sudo('./mount_keys.sh')
    #mounted = exists('/Volumes/keys')


def chmod(permission, file, dir=False):
    if dir:
        sudo("chmod -R %s %s" % (permission, file))
    else:
        sudo("chmod %s %s" % (permission, file))


def unzip(filename):
    sudo('unzip %s' % filename)


def untar(filename):
    sudo('tar xvzf {file}.tar.gz'.format(file=filename))


@task
def set_device_id():
    device_id = get_device_id()
    device_match_replace = "s/DEVICE_ID.*/DEVICE_ID\ =\ \'{dev_id}\'/g".format(dev_id=device_id)
    dev_settings = 'settings_devid.py'
    with cd(SETTINGS_DIR):
        sudo("sed %s settings.py >%s" % (device_match_replace, dev_settings))
        sudo("mv %s settings.py" % dev_settings)
        chmod('755', 'settings.py')
        sudo('chown -R Django:staff settings.py')


def _timestamp():
    return datetime.datetime.fromtimestamp(time.time).strftime('%Y%m%d_%H%M%S')


def get_device_id():
    last_bit = hostname()[0][-2:]
    id = int(last_bit)
    if id < 10:
        id += 80
        print(green("The device id: {}".format(id)))
        return id
    return id


def hostname():
    hostname = sudo('hostname')
    return (hostname, env.host,)


def exit_if_not_installed(prog_name):
    if program_not_installed(prog_name):
        print(red("'%s' please install '%s' before continuing" % (env.host, prog_name)))
        abort("Halted on host:[%s]" % env.host)


def program_is_installed(prog_name):
    return not program_not_installed(prog_name)


def program_not_installed(prog_name):
    not_installed = False
    with quiet():
        if sudo('which %s' % prog_name).failed:
            print "%s is not installed on %s" % (prog_name, env.host)
            not_installed = True
    return not_installed


@task
def change_to_setswana():
    change_language(current='en', to='tn')


@task
def change_to_english():
    change_language(current='tn', to='en')


def change_language(current=None, to=None):
    current_lang = "LANGUAGE_CODE = '%s'" % current
    new_lang = "LANGUAGE_CODE = '%s'" % to
    replacement = [(current_lang, new_lang)]
    modify_settings(replacement)


def modify_settings(replacements):
    "replacement should be a list of tuples"
    get(SETTINGS_FILE, 'settings.py')
    with open('settings.py', 'r') as old_settings:
        content = old_settings.read()
        for pair in replacements:
            content = content.replace(pair[0], pair[1])
        #content = old_settings.read().replace(current_lang, new_lang)
        with open('settings.py', 'w') as settings:
            settings.write(content)
    put('settings.py', SETTINGS_FILE, use_sudo=True)
    os.remove('settings.py')
    with cd(SETTINGS_DIR):
        chmod('755', 'settings.py')
        sudo('chown -R Django:staff settings.py')


@task
def apache_setup():
    #prevent mysql from misbehaving
    #with warn_only():
        #sudo('ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.18.dylib')
    #the httpd.conf file
    put(a_file(FAB_APACHE_DIR, 'httpd.conf'), '/etc/apache2/httpd.conf', use_sudo=True)
    #configure the http-vhosts.conf file
    put(a_file(FAB_APACHE_DIR, 'httpd-vhosts.conf'),
        '/etc/apache2/extra/httpd-vhosts.conf', use_sudo=True)
    #create vhosts directory
    mkdir('/etc/apache2/extra/vhosts', as_sudo=True)
    #copy the localhost config and bcppstudy vhosts config
    put(a_file(FAB_APACHE_DIR, 'localhost.conf'), '/etc/apache2/extra/vhosts/localhost.conf', use_sudo=True)
    put(a_file(FAB_APACHE_DIR, 'bcppstudy.conf'), '/etc/apache2/extra/vhosts/bcppstudy.conf', use_sudo=True)
    #make required directories
    mkdir('~/Sites/logs')
    mkdir('~/Sites/localhost')
    mkdir('~/Sites/bcppstudy/static')
    #setup the bcppstudy in hosts
    put(a_file(FAB_APACHE_DIR, 'hosts'), '/etc/hosts', use_sudo=True)
    #put the right permissions on local folder for apache access
    chmod('755', '~/source/bhp066_project/bhp066/bhp066')
    chmod('755', '~/Sites/bcppstudy')
    #set the STATIC_ROOT in the settings file
    changes = [("STATIC_ROOT = PROJECT_DIR.child('static')", "STATIC_ROOT = '/Users/django/Sites/bcppstudy/static/'")]
    changes += [("MAP_DIR = STATIC_ROOT.child('img')", "MAP_DIR = '/Users/django/Sites/bcppstudy/static/img/'")]
    modify_settings(changes)
    #run collectstatic
    manage_py('collectstatic')
    #restart apache
    print(green('Restarting Apache .....'))
    sudo('apachectl -k graceful')
