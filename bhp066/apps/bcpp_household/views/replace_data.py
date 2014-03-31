from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import Household, Plot
from ..helpers import ReplacementHelper


def replace_data(request, survey):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    replace_str = ''
    template = 'replacement_data.html'
    replacement_data = ReplacementHelper(survey).replaceable_households(survey)
#     replacement_data = ReplacementHelper(survey).replaceable_households(survey)
    for item in replacement_data:
        if isinstance(item[0], Plot):
            replace_str = replace_str + ',' + item[0].plot_identifier
        elif isinstance(item[0], Household):
            replace_str = replace_str + ',' + item[0].household_identifier
    return render_to_response(
            template, {
                'replacement_data': replacement_data,
                'replace_str': replace_str,
                'replacement_count': len(replacement_data),
                },
                context_instance=RequestContext(request)
            )
