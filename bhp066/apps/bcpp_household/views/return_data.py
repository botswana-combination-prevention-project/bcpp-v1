from datetime import datetime
import itertools

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..helpers import ReplacementHelper
from ..models import Household, Plot, ReplacementHistory


def return_data(request):
    replacement_data = None
    replacement_data_list = []
    replacement_count = 0
    plot = None
    household = None
    replacement_reason = None
    template = 'return_data.html'
    message = None
    replacement_plots = Plot.objects.filter(selected=2, replacement=None)
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
            print replacement_data
            replacement_data = replacement_data.split(',')
            replacement_data.pop(0)
            content_type = None
            print replacement_data
            for item in replacement_data:
                if replacement_plots and len(replacement_plots) > replacement_count:
                    replacing_plot = replacement_plots[replacement_count]
                    if not replacing_plot.replacement:
                        if Household.objects.get(household_identifier=item):
                            household = Household.objects.get(household_identifier=item)
                            replacement_reason = ReplacementHelper().replacement_reason(household)
                        else:
                            plot = Plot.objects.get(plot_identifier=item)
                            replacement_reason = ReplacementHelper().replacement_reason(plot)
                        if household:
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            household.replacement = replacing_plot.plot_identifier
                            household.save()
                            replacing_plot.replacement = household.household_identifier
                            replacing_plot.save()
                            ReplacementHistory.objects.create(replacing_item=replacing_plot.plot_identifier, replaced_item=item, replacement_datetime=datetime.now(), replacement_reason=replacement_reason,)
                        else:
                            replacement_data_list.append(replacing_plot.plot_identifier)
                            plot.replacement = replacing_plot.plot_identifier
                            plot.save()
                            replacing_plot.replacement = plot.plot_identifier
                            replacing_plot.save()
                            ReplacementHistory.objects.create(replacing_item=replacing_plot.plot_identifier, replaced_item=plot, replacement_datetime=datetime.now(), replacement_reason=replacement_reason,)
                    elif not plot.is_dispatched:
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
                        plot = Plot.objects.get(household_identifier=household.replacement_plot)
                        replacement_data_list.append(plot.plot_identifier)
                pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_data_list})).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(Plot)
                return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
