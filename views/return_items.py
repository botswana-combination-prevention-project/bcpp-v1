from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_sync.models import Producer
from bhp_dispatch.classes import DispatchController
from bhp_dispatch.models import DispatchItem


@login_required
def return_items(request, **kwargs):
    """ Update the device dispatch and hbc dispatch items as checked in
    """
    #TODO: Update netbook/device as checked in as well
    if not 'ALLOW_MODEL_CHECKOUT' in dir(settings):
        messages.add_message(request, messages.ERROR, 'ALLOW_MODEL_CHECKOUT global boolean not found in settings.')
    producer = None
    #if kwargs.get('device'):
    try:
        producer = Producer.objects.get(name__iexact=kwargs.get('producer'))
#        DispatchController('default', producer.name, action='returning').return_from_producer(producer)
#        messages.add_message(
#                request,
#                messages.INFO,
#                'Returning dispatched items from device {0}.'.format(producer.name)
#                )
        if not 'default' in settings.DATABASES.keys():
            raise AttributeError('Cannot find key "server" in settings.DATABASES. '
                                 'Please add and try again.')
        message_list = DispatchController('default', producer.name, action='returning').return_from_producer(producer)
#            dispatch_controller = DispatchController(True, producer)
        # Check that we have have households checked for this device
#        dispatched_items = DispatchItem.objects.filter(producer=producer)
#        if dispatched_items:
#        if False:
#            pass
        for msg in message_list:
            messages.add_message(
                    request,
                    messages.INFO,
                    msg
                    )
#
#            for dispatch in dispatched_items:
#                #Update checkout and hbc dispatch items
#                #dispatch_controller.dispatch(dispatch)
#                dispatch.unlock_dispatch_item()
#
#                messages.add_message(
#                    request,
#                    messages.INFO,
#                    'Unlocked {0} where {1}={2}.'.format(dispatch.dispatch_container.container_model_name,
#                                                         dispatch.dispatch_container.container_identifier_attrname,
#                                                         dispatch.dispatch_container.container_identifier)
#                    )
#        else:
#            messages.add_message(
#                    request,
#                    messages.INFO,
#                    'Device {0} does not have any dispatched households.'.format(producer.name)
#                    )
    except ObjectDoesNotExist:
        raise Http404
    except:
        raise

    return render_to_response(
        'checkin_households.html', {'producer': producer, },
        context_instance=RequestContext(request)
        )
