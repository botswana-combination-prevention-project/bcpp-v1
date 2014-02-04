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
    message = None
    replacement_plots = Plot.objects.filter(selected=2, replacement=False)
    if not replacement_plots:
        message = 'No plots available to replace with.'
        return render_to_response(
                template, {
                    'message': message,
                    },
                    context_instance=RequestContext(request)
                )
    else:
        if request.GET.get('replace_str'):
            replacement_data = request.GET.get('replace_str')
            replacement_data = replacement_data.split(',')
            replacement_data.pop(0)
            #return households
            #TODO: Call return method to return households
            #get replacement plots
            replacement_count = 0
            content_type = None
            for household in replacement_data:
                if replacement_plots and len(replacement_plots) > replacement_count:
                    replacement_data_list.append(replacement_plots[replacement_count].plot_identifier)
                    house = Household.objects.get(household_identifier=household)
                    house.replacement = True
                    house.save()
                    replacement_plots[replacement_count].replacement = True
                    replacement_plots[replacement_count].save()
                    replacement_count += 1
            pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
            selected = list(itertools.chain(*pks))
            content_type = ContentType.objects.get_for_model(Plot)
            return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
        else:
            if request.GET.get('household_identifier'):
                household_id = request.GET.get('household_identifier')
                #return households
                #TODO: Call return method to return households
                if replacement_plots:
                    replacement_data_list.append(replacement_plots[0].plot_identifier)
                    house = Household.objects.get(household_identifier=household_id)
                    house.replacement = True
                    house.save()
                    replacement_plots[0].replacement = True
                    replacement_plots[0].save()
                pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(Plot)
                return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))