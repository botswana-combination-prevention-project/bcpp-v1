from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from edc.device.dispatch.models import DispatchContainerRegister

from ..models import HouseholdStructure
from ..classes import ReplacementData


def replace_data(request, survey):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    replacement_data = []
    replace_str = ''
    template = 'replacement_data.html'
    household_structures = HouseholdStructure.objects.filter(household__plot__selected__in=[1, 2])
    
    #Get all household to be replaced
    replacement_data = ReplacementData(survey).get_replaceable_items_for_view()

    
    replacement_count = len(replacement_data)
    
    #[household, reason, producer]
    for item in replacement_data:
        if isinstance(item[0], Plot):
            replace_str = replace_str + ',' + item[0].plot_identifier
        elif isinstance(item[0], Household):
            replace_str = replace_str + ',' + item[0].household_identifier
    return render_to_response(
            template, {
                'replacement_data': replacement_data,
                'replace_str': replace_str,
                'replacement_count': replacement_count,
                },
                context_instance=RequestContext(request)
            )
