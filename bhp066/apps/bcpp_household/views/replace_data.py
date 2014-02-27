from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from ..models import Plot, Household
from ..classes import ReplacementData

def replace_data(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    replacement_data = []
    replace_str = ''
    replacement_count = 0
    template = 'replacement_data.html'
    plots = Plot.objects.filter(Q(selected=2) | Q(selected=1))
    #Get all household to be replaced
    for plot in plots:
        if ReplacementData().replace_refusals(plot):
            replacement_data = replacement_data + ReplacementData().replace_refusals(plot)
        if ReplacementData().replacement_absentee(plot):
            replacement_data = replacement_data + ReplacementData().replacement_absentee(plot)
    replacement_count = len(replacement_data)
    for household in replacement_data:
        replace_str = replace_str + ',' + household.household_identifier
        household.replacement = True
        household.save()
    return render_to_response(
            template, {
                'replacement_data': replacement_data,
                'replace_str': replace_str,
                'replacement_count': replacement_count,
                },
                context_instance=RequestContext(request)
            )
