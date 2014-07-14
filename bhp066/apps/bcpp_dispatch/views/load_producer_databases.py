from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.device.sync.models import Producer


def load_producer_databases(request, **kwargs):
    """Add all producer database settings to the setting's file 'DATABASE' attribute."""
    template = 'load_producer_databases.html'
    message = "No producers added. The producer table may be empty"
    producers = Producer.objects.all()
    if producers:
        for producer in producers:
            settings.DATABASES[producer.settings_key] = {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB',
                },
                'NAME': producer.db_user_name,
                'USER': producer.db_user,
                'PASSWORD': producer.db_password,
                'HOST': producer.producer_ip,
                'PORT': producer.port,
            }
        message = "{0} producer database settings added to the DATABASE settings attribute.".format(producers.count())

    return render_to_response(
            template, {
                'message': message,
            },
            context_instance=RequestContext(request))
