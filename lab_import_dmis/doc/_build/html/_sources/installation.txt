Installation
============

..note: This module works together with :mod:`lab_import_lis`.

Checkout the latest version of :mod:`lab_import_dmis`::

    svn co http://192.168.1.50/svn/lab_import_dmis

Add :mod:`lab_import_dmis` to your project ''settings'' file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django_extensions',
        'audit_trail',
        'bhp_base_model',
        'bhp_common',
        'lab_import_dmis',
        ...
        )
      

:mod:`lab_import_dmis` accesses the DMIS which uses an MSSQL database. Add this to your
settings::

    # for bhp_import_dmis
    if platform.system() == 'Darwin':
        LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER=/usr/local/lib/libtdsodbc.so;SERVER=192.168.1.141;'
                                      'PORT=1433;UID=sa;PWD=cc3721b;DATABASE=BHPLAB')
    else:
        LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;'
                                       'DATABASE=BHPLAB')
      
Each import session is recorded and grouped by a "lock name". Add this to your settings::
    
    LABDB = 'bhplab'
    LAB_LOCK_NAME = 'BHP041'
