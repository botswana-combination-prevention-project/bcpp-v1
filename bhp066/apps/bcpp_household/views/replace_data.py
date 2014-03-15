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
    replacement_producer = []
    plot_identifiers = []
    replace_str = ''
    template = 'replacement_data.html'
    plots = Plot.objects.filter(Q(selected=2) | Q(selected=1))
    #Get all household to be replaced
    for plot in plots:
        if ReplacementData().replace_refusals(plot):
            replacement_data = replacement_data + ReplacementData().replace_refusals(plot)  # replacement of refusals.
            plot_identifiers.append(plot.plot_identifier)
        if ReplacementData().replacement_absentees_ineligibles(plot):
            replacement_data = replacement_data + ReplacementData().replacement_absentees_ineligibles(plot)  # replacement of absentees.
            plot_identifiers.append(plot.plot_identifier)
        if ReplacementData().is_replacement_valid(plot):
            replacement_data = replacement_data + ReplacementData().is_replacement_valid(plot)  # replacement of an invalid replacement.
    replacement_count = len(replacement_data)
    # For all items attach it to the produce where it has been dispatch to.
    for identifier in plot_identifiers:
        container = DispatchContainerRegister.objects.get(container_identifier=identifier)
        plot = Plot.objects.get(plot_identifier=identifier)
        household = Household.objects.get(plot=plot)
        replacement_producer.append([household.household_identifier, container.producer])
    for item in replacement_data:
        if isinstance(item, Plot):
            replace_str = replace_str + ',' + item.plot_identifier
        elif isinstance(item, Household):
            replace_str = replace_str + ',' + item.household_identifier
    return render_to_response(
            template, {
                'replacement_data': replacement_data,
                'replace_str': replace_str,
                'replacement_count': replacement_count,
                'replacement_producer': replacement_producer,
                },
                context_instance=RequestContext(request)
            )
