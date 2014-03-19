import itertools
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext

from django.http import HttpResponseRedirect

from django.db.models import Q

from ..models import Plot, Household


def return_data(request):
    replacement_data = None
    replacement_data_list = []
    replacement_count = 0
    template = 'return_data.html'
    message = None
    replacement_plots = Plot.objects.filter(selected=2, replacing_household=None)
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
            content_type = None
            for household in replacement_data:
                if replacement_plots and len(replacement_plots) > replacement_count:
                    if not replacement_plots[replacement_count].replacement:
                        replacement_data_list.append(replacement_plots[replacement_count].plot_identifier)
                        house = Household.objects.get(household_identifier=household)
                        house.replacement_plot = replacement_plots[replacement_count].plot_identifier
                        house.save()
                        replacement_plots[replacement_count].replacement = house.household_identifier
                        replacement_plots[replacement_count].save()
                    else:
                        house = Household.objects.get(household_identifier=household)
                        if not house.is_dispatched:
                            plot = Plot.objects.get(household_identifier=house.replacement_plot)
                            replacement_data_list.append(plot.plot_identifier)
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
                if replacement_plots and len(replacement_plots) > replacement_count:
                    if not replacement_plots[replacement_count]:
                        replacement_data_list.append(replacement_plots[replacement_count].plot_identifier)
                        house = Household.objects.get(household_identifier=household_id)
                        house.replacement_plot = replacement_plots[replacement_count].plot_identifier
                        house.save()
                        replacement_plots[replacement_count].replacement = house.household_identifier
                        replacement_plots[replacement_count].save()
                    else:
                        house = Household.objects.get(household_identifier=household_id)
                        if not house.is_dispatched:
                            plot = Plot.objects.get(household_identifier=house.replacement_plot)
                            replacement_data_list.append(plot.plot_identifier)
                pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(Plot)
                return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
