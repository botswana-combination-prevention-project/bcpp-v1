import itertools
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext

from django.http import HttpResponseRedirect

from django.db.models import Q

from ..models import Household
from ..models import Plot
from ..models import ReplacementHistory


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
            content_type = None
            for item, reason , producer in replacement_data:
                if replacement_plots and len(replacement_plots) > replacement_count:
                    replacing_plot = replacement_plots[replacement_count]
                    if not replacing_plot.replacement:
                        if isinstance(Household, item):
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            item.replacement = replacing_plot.plot_identifier
                            item.save()
                            replacing_plot.replacement = item.household_identifier
                            replacing_plot.save()
                            ReplacementHistory.objects.create(replacing_item=replacing_plot.household_identifier, replaced_item=item, replacement_datetime='', replacement_reason=reason,)
                        else:
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            item.replacement = replacing_plot.plot_identifier
                            item.save()
                            replacing_plot.replacement = item.plot_identifier
                            replacing_plot.save()
                            ReplacementHistory.objects.create(replacing_item=replacing_plot.plot_identifier, replaced_item=item, replacement_datetime='', replacement_reason=reason,)
                    elif not item.is_dispatched:
                        replacement_data_list.append(replacing_plot.plot_identifier)
                replacement_count += 1
            pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
            selected = list(itertools.chain(*pks))
            content_type = ContentType.objects.get_for_model(Plot)
            return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
        else:
            if request.GET.get('item_identifier'):
                item_identifier = request.GET.get('item_identifier')
                item = None
                if replacement_plots and len(replacement_plots) > 1:
                    replacing_plot = replacement_plots[0]
                    if not replacing_plot.replacement:
                        if Household.objects.filter(household_identifier=item_identifier):
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            item = Household.objects.get(household_identifier=item_identifier)
                            item.replacement_plot = replacement_plots[replacement_count].plot_identifier
                            item.save()
                            replacing_plot.replacement = item.household_identifier
                            replacing_plot.save()
                        elif Plot.objects.filter(plot_identifier=item_identifier):
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            item = Plot.objects.get(plot_identifier=item_identifier)
                            item.replacement_plot = replacement_plots[replacement_count].plot_identifier
                            item.save()
                            replacing_plot.replacement = item.household_identifier
                            replacing_plot.save()
                    elif not item.is_dispatched:
                        plot = Plot.objects.get(household_identifier=house.replacement_plot)
                        replacement_data_list.append(plot.plot_identifier)
                pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(Plot)
                return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
