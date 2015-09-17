from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from edc.device.dispatch.models import DispatchContainerRegister


@login_required
def return_households(request, **kwargs):
    """ Update the device dispatch and hbc dispatch items as checked in
    """

    household_identifier = kwargs.get('household')
    ref_container = DispatchContainerRegister.objects.get(
        container_app_label='bcpp_household',
        container_model_name='household',
        container_identifier_attrname='household_identifier',
        container_identifier=household_identifier,
    )
    all_containers = DispatchContainerRegister.objects.filter(
        container_model_name='household',
        container_identifier_attrname='household_identifier',
        producer=ref_container.producer,
        is_dispatched=True,)

    return render_to_response(
        'household_return.html', {
            'queryset': all_containers,
            'producer': ref_container.producer.name
        },
        context_instance=RequestContext(request)
    )
