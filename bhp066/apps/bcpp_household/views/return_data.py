from datetime import datetime
import itertools

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..helpers import ReplacementHelper
from ..models import Household, Plot


def return_data(request):
    content_type = None
    replaceble_households = []
    replaceble_plots = []
    replacement_items = []
    plot = None
    household = None
    template = 'return_data.html'
    message = None
    replacement_plots = Plot.objects.filter(selected=2, replaces=None)
    if not replacement_plots:
        message = 'No plots available to replace with.'
        return render_to_response(
                template, {
                    'message': message,
                    },
                    context_instance=RequestContext(request)
                )
    else:
        if request.GET.get('replaceble_household_str'):
            replaceble_households_identifiers = request.GET.get('replaceble_household_str')
            replaceble_households_identifiers = replaceble_households_identifiers.split(',')
            replaceble_households_identifiers.pop(0)
            for identifer in replaceble_households_identifiers:
                household = Household.objects.get(household_identifier=identifer)
                replaceble_households.append(household)
            replacement_helper = ReplacementHelper()
            replacement_plots = replacement_helper.replace_household(replaceble_households)
        if request.GET.get('replaceble_plot_str'):
            replaceble_plot_identifiers = request.GET.get('replaceble_plot_str')
            replaceble_plot_identifiers = replaceble_plot_identifiers.split(',')
            replaceble_plot_identifiers.pop(0)
            content_type = None
            replaceble_plots = []
            for identifer in replaceble_plot_identifiers:
                plot = Plot.objects.get(plot_identifier=identifer)
                replaceble_plots.append(plot)
            replacement_helper = ReplacementHelper()
            replacement_plots = replacement_helper.replace_plot(replaceble_plots)
#             if not plot.is_dispatched:
#                 replaceble_items.append(replacing_plot.plot_identifier)
#                 replacement_count += 1
        replacement_items = replacement_plots + replaceble_households
        pks = replacement_items.values_list('pk')
        selected = list(itertools.chain(*pks))
        content_type = ContentType.objects.get_for_model(Plot)
        return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
#     else:
#         pass
#             if request.GET.get('item_identifier'):
#                 item_identifier = request.GET.get('item_identifier')
#                 item = None
#                 if replacement_plots and len(replacement_plots) > 1:
#                     replacing_plot = replacement_plots[0]
#                     if not replacing_plot.replacement:
#                         if Household.objects.filter(household_identifier=item_identifier):
#                             replacement_data_list.append(replacing_plot.plot_identifier)
#                             item = Household.objects.get(household_identifier=item_identifier)
#                             item.replacement_plot = replacement_plots[replacement_count].plot_identifier
#                             item.save()
#                             replacing_plot.replacement = item.household_identifier
#                             replacing_plot.save()
#                         elif Plot.objects.filter(plot_identifier=item_identifier):
#                             replacement_data_list.append(replacing_plot.plot_identifier)
#                             item = Plot.objects.get(plot_identifier=item_identifier)
#                             item.replacement_plot = replacement_plots[replacement_count].plot_identifier
#                             item.save()
#                             replacing_plot.replacement = item.household_identifier
#                             replacing_plot.save()
#                     elif not item.is_dispatched:
#                         plot = Plot.objects.get(household_identifier=household.replacement_plot)
#                         replacement_data_list.append(plot.plot_identifier)
#                 pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
#                 selected = list(itertools.chain(*pks))
#                 content_type = ContentType.objects.get_for_model(Plot)
#                 return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
