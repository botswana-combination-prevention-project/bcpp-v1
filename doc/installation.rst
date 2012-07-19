Installation
============

Checkout the latest version of :mod:`bhp_device` into your test environment project folder::

    svn co http://192.168.1.50/svn/bhp_device

Add :mod:`bhp_device` to your project ''settings'' file::

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
        'bhp_device',
        ...
        )

Add these attributes to the bottom of your project ''settings'' file::

    # a number that is unque amongst the devices running the EDC
    DEVICE_ID=31
    # optional, default is 2
    # DEVICE_ID_LENGTH=2
    # optional, may also be specified in :mod:`bhp_variables`
    # HOSTNAME_PREFIX='mpp'

    
        