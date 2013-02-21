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
        messages.add_message(
                request,
                messages.INFO,
                'Returning dispatched items from device {0}.'.format(producer.name)
                )
        
#            dispatch_controller = DispatchController(True, producer)
        # Check that we have have households checked for this device
        dispatched_items = DispatchItem.objects.filter(producer=producer)
        if dispatched_items:
            messages.add_message(
                    request,
                    messages.INFO,
                    'Found {0} dispatch(es).'.format(len(dispatched_items))
                    )

            for dispatch in dispatched_items:
                #Update checkout and hbc dispatch items
                #dispatch_controller.dispatch(dispatch)
                dispatch.unlock_dispatch_item()

                messages.add_message(
                    request,
                    messages.INFO,
                    'Checked in {0}.'.format(dispatch.item_identifier)
                    )
        else:
            messages.add_message(
                    request,
                    messages.INFO,
                    'Device {0} does not have any dispatched households.'.format(producer.name)
                    )
    except ObjectDoesNotExist:
        raise Http404
    except:
        raise

    return render_to_response(
        'checkin_households.html', {'producer': producer, },
        context_instance=RequestContext(request)
        )
