from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from bcpp_household.models import Household
from bhp_dispatch.models import DispatchContainerRegister


@login_required
def return_households(request, **kwargs):
    container_register = DispatchContainerRegister.objects.get(container_model_name='household',
                                                               container_identifier=kwargs.get('household'),
                                                               is_dispatched=True)
    dispatched_containers = DispatchContainerRegister.objects.filter(producer=container_register.producer,
                                                                     is_dispatched=True)
    dispatched_households = []
    for container in dispatched_containers:
        dispatched_households.append(Household.objects.get(household_identifier=container.container_identifier))
    return render(request, 'household_return.html', {
        'producer': container_register.producer,
        'dispatched_households': dispatched_households,
        })
