from fabric.api import *
from fabric.contrib.files import exists
from django.contrib.auth.models import User


env.dbname = 'bhp066'
env.mysql_root_passwd = 'cc3721b'

env.hosts = ['192.168.1.22']
env.user = 'django'
env.password = 'django'

SRC_DIR = 'source'
PROJECT_ROOT = '~/source/bhp066_project'
PROJECT_DIR = '~/source/bhp066_project/bhp066'
EDC_DIR = '%s/edc' % PROJECT_DIR
LIS_DIR = '%s/lis' % PROJECT_DIR
VIRTUALENV = 'bhp066_env'
VIRTUALENV_HOME = '~/.virtualenvs'
SETTINGS_DIR = '{projdir}/bhp066'.format(projdir=PROJECT_DIR)
FILE_WITH_SOUTH = '%s/settings.py' % SETTINGS_DIR
UNSOUTHED = 'unsouthed'

WORKON_VIRTUALENV = 'workon {virtualenv}'.format(virtualenv=VIRTUALENV)

GIT_PULL = 'git pull origin master'
git_clone = 'git clone git@gitserver:{repo}.git'.format


@task
def deploy2_mysql():
    execute(prepare_code)
    comment_out_south()
    syncdb(UNSOUTHED)
    uncomment_south()
    syncdb()
    fake_migration()


@task
def prepare_code():
    execute(check_for_required_programs)
    checkout_code()
    setup_virtualenv()


@task
def check_for_required_programs():
    exit_as_not_installed('python')
    exit_as_not_installed('git')
    if program_not_installed('pip'):
        sudo('easy_install -U pip')
    exit_as_not_installed('mysql')
    exit_as_not_installed('swig')
    print "Success: Required programs are installed"


def checkout_code():
    if project_is_checked_out():
        execute(update_code)
    else:
        execute(clone_code)


@task
def clone_code():
    if not exists(SRC_DIR):
        mkdir(SRC_DIR)
    run('rm -rf %s/*' % SRC_DIR)
    with cd(SRC_DIR):
        run(git_clone(repo='bhp066_project'))
    with cd(PROJECT_DIR):
        run(git_clone(repo='edc'))
        run(git_clone(repo='lis'))


def project_is_checked_out():
    return exists(EDC_DIR) and exists(LIS_DIR)


@task
def update_code():
    with cd(PROJECT_ROOT):
        run(GIT_PULL)
    with cd(EDC_DIR):
        run(GIT_PULL)
    with cd(LIS_DIR):
        run(GIT_PULL)


def setup_virtualenv():
    if not virtualenv_exists():
        execute(install_virtualenv)
        create_virtualenv()
    install_dependencies()


@task
def install_virtualenv():
    pip_install('virtualenv')
    if not exists(VIRTUALENV_HOME):
        mkdir(VIRTUALENV_HOME)
    pip_install('virtualenvwrapper')
    put('.bash_profile', '.bash_profile')


def create_virtualenv():
    run('mkvirtualenv bhp066_env')


def install_dependencies():
    with prefix(WORKON_VIRTUALENV):
        pip_install('-r %s/requirements.txt' % PROJECT_ROOT)


def virtualenv_exists():
    return exists('%s/%s' % (VIRTUALENV_HOME, VIRTUALENV))


def syncdb(settings_file=None):
    manage_py('syncdb --noinput', settings_file)


def fake_migration(settings_file=None):
    manage_py('migrate --fake', settings_file)


def manage_py(command=None, config=None):
    with cd(PROJECT_DIR):
        with prefix(WORKON_VIRTUALENV):
            sudo('chmod a+x manage.py')
            with settings(warn_only=True):
                if config:
                    sudo('./manage.py {command} --settings=bhp066.{config}'.format(command=command, config=config))
                else:
                    sudo('./manage.py {command}'.format(command=command))


def create_superuser():
    details = dict(password='cc3721b', is_staff=True, is_active=True, is_superuser=True)
    user, created = User.objects.get_or_create(username='username', defaults=details)


def comment_out_south():
    with cd(SETTINGS_DIR):
        sudo("sed \"s/'south'/\#'south'/g\" settings.py >%s.py" % UNSOUTHED)


def uncomment_south():
    with cd(SETTINGS_DIR):
        #sudo("sed \"s/#'south'/'south'/g\" unsouthed.py >settings.py")
        sudo('rm %s.py' % UNSOUTHED)


@task
def set_mysql_passwd():
    sudo('mysqladmin -u root password %s' % env.mysql_root_passwd)


@task
def create_db():
    create_db_sql = "CREATE DATABASE {dbname}".format(dbname=env.dbname)
    mysql_execute(create_db_sql)


def mysql_execute(cmd):
    credentials = 'mysql -u root --password={password}'.format(password=env.mysql_root_passwd)
    full_command = 'echo "{sql_command}" | {on_mysql}'.format(sql_command=cmd, on_mysql=credentials)
    sudo(full_command)


def mkdir(dirname, as_sudo=True):
    mkdir_cmd = 'mkdir {dir}'.format(dir=dirname)
    if as_sudo:
        sudo(mkdir_cmd)
    else:
        run(mkdir_cmd)


def pip_install(package_name, as_sudo=True):
    install_cmd = 'pip install {package}'.format(package=package_name)
    if as_sudo:
        sudo(install_cmd)
    else:
        run(install_cmd)


def exit_as_not_installed(prog_name):
    if program_not_installed(prog_name):
        abort("Please install %s on %s first before continuing" % (prog_name, env.host))


def program_not_installed(prog_name):
    not_installed = False
    with quiet():
        if run('which %s' % prog_name).failed:
            print "%s is not installed on %s" % (prog_name, env.host)
            not_installed = True
    return not_installed
