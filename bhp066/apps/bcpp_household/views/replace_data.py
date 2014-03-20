from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from edc.device.dispatch.models import DispatchContainerRegister

from ..models import Plot, Household
from ..classes import ReplacementData


def replace_data(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    replacement_data = []
    replace_str = ''
    template = 'replacement_data.html'
    plots = Plot.objects.filter(Q(selected=2) | Q(selected=1))
    #Get all household to be replaced
    for plot in plots:
        if ReplacementData().check_refusals(plot):
            replacement_data = replacement_data + ReplacementData().check_refusals(plot)  # replacement of refusals.
        if ReplacementData().check_absentees_ineligibles(plot):
            replacement_data = replacement_data + ReplacementData().check_absentees_ineligibles(plot)  # replacement of absentees.
        if ReplacementData().is_replacement_valid(plot):
            replacement_data = replacement_data + ReplacementData().is_replacement_valid(plot)  # replacement of an invalid replacement.
    replacement_count = len(replacement_data)
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
