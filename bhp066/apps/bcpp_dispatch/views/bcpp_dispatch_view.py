from apps.bcpp_dispatch.classes import BcppDispatchController
from apps.bcpp_dispatch.forms import BcppDispatchForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from edc.device.dispatch.views import dispatch

from edc.device.sync.models import Producer


@login_required
@csrf_protect
def bcpp_dispatch_view(request, **kwargs):
    """Receives a list of item identifiers, load all producers database settings and user selects the producer to dispatch to."""
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
    return dispatch(request, BcppDispatchController, BcppDispatchForm, app_name='bcpp', **kwargs)
