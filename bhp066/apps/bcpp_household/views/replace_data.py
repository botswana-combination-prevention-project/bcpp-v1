from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from ..models import Plot, Household
from ..classes import ReplacementData

def replace_data(request):

    replacement_data = {}
    replacement_data_list = []
    replacement_count = 0
    template = 'replacement_data.html'
    plots = Plot.objects.filter(Q(selected=2) | Q(selected=1))
    #Get all household to be replaced
    for plot in plots:
        if ReplacementData().replace_refusals(plot):
            replacement_data.update(ReplacementData().replace_refusals(plot))
        if ReplacementData().replacement_absentee(plot):
            replacement_data.update(ReplacementData().replacement_absentee(plot))
        if ReplacementData().replacement_none_consented(plot):
            replacement_data.update(ReplacementData().replacement_none_consented(plot))
    replacement_count = len(replacement_data)
    for plot, household in replacement_data.iteritems():
        replacement_data_list.append(household.household_identifier)
        plot.replacement = True
        household.replacement = True
        plot.save()
        household.save()
    print replacement_data_list
    return render_to_response(
            template, {
                'replacement_data': replacement_data_list,
                'replacement_count': replacement_count,
                },
                context_instance=RequestContext(request)
            )
