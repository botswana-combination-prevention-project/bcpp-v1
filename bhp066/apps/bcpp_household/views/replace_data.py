from django.shortcuts import render_to_response
from django.template import RequestContext

from ..helpers import ReplacementHelper


def replace_data(request, survey):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    replaceble_households_str = ''
    replaceble_plots_str = ''
    template = 'replacement_data.html'
    replacement_households = ReplacementHelper().replaceable_households(survey)
    replacement_plots = ReplacementHelper().replaceable_plots()
    replacebles = replacement_households + replacement_plots
    for household in replacement_households:
        replaceble_households_str = replaceble_households_str + ',' + household.household_identifier
    for plot in replacement_plots:
        replaceble_plots_str = replaceble_plots_str + ',' + plot.plot_identifier
    return render_to_response(
            template, {
                'replacement_data': replacebles,
                'replaceble_households_str': replaceble_households_str,
                'replaceble_plots_str': replaceble_plots_str,
                'replacement_count': len(replacebles),
                },
                context_instance=RequestContext(request)
            )
