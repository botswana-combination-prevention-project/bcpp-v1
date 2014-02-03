import itertools
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

from django.db.models import Q

from ..models import Plot, Household
from ..classes import ReplacementData
from ..exceptions import ReplacementError

def return_data(request):
    replacement_data = None
    replacement_data_list = []
    replacement_count = 0
    template = 'return_data.html'

    if request.GET.get('replacement_data'):
        replacement_data = request.GET.get('replacement_data')
        print replacement_data
        print replacement_data[2:-1]
        print replacement_data[1]
        print replacement_data[-1]
        replacement_data = replacement_data[2:-1]
        print replacement_data
        
        #return households
        #TODO: Call return method to return households
        #get replacement plots
        replacement_plots = Plot.objects.filter(selected=2)
        print "Plots"
        print replacement_plots
        print "Plots"
        replacement_count = 0
        content_type = None
        while replacement_count < len(replacement_data):
            for household in replacement_data:
                if replacement_plots[replacement_count]:
                    replacement_data_list.append(replacement_plots[replacement_count].plot_identifier)
                    plot.replacement = True
                    plot.save
                    household.replacement = True
                    household.save()
                    replacement_plots[replacement_count].replacement = True
                    replacement_plots[replacement_count].save()
                    household_rep = Household.objects.get(plot=replacement_plots[replacement_count])
                    household_rep.replacement = True
                    household_rep.save()
                    replacement_count += 1
                else:
                    raise ReplacementError("There are no more Plots available to replace with.")
    pks = Plot.objects.filter(selected=2).values_list('pk')
    selected = list(itertools.chain(*pks))
    #selected = replacement_data_list
    content_type = ContentType.objects.get_for_model(Plot)
    return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))


#     elif request.GET.get('plot') and request.GET.get('household'):
#         plot = request.GET.get('plot')
#         household = request.GET.get('household')
#         return render_to_response(
#                 template, {
#                     'replacement_data': replacement_data_list,
#                     'replacement_count': replacement_count,
#                     },
#                     context_instance=RequestContext(request)
#                 )
#     else:
#         return render_to_response(
#                 template, {
#                     'replacement_data': replacement_data_list,
#                     'replacement_count': replacement_count,
#                     },
#                     context_instance=RequestContext(request)
#                 )