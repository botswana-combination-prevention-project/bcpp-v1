from django.shortcuts import render_to_response
from django.template import RequestContext

from ..helpers import ReplacementHelper


def check_replacements(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    template = 'check_replacements.html'
    replaceables = []
    message = None
    producer_name = request.POST.get('producer_name')
    if producer_name:
        replacement_helper = ReplacementHelper()
        replaceables = replacement_helper.replaceable_households(producer_name) + replacement_helper.replaceable_plots(producer_name)
    if not replaceables:
        message = "There are no replaceable households or plots from {}".format(str(producer_name))
    return render_to_response(
        template, {
            'replaceables': replaceables,
            'replacement_count': len(replaceables),
            'producer_name': producer_name,
            'message': message,
            },
        context_instance=RequestContext(request)
        )
