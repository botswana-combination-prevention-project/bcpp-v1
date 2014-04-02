import itertools

from django.contrib.contenttypes.models import ContentType
from django.db.models import Min
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.bcpp_survey.models import Survey

from ..helpers import ReplacementHelper
from ..models import Plot


def return_data(request):
    content_type = None
    replaceble_plots = []
    replacement_items = []
    template = 'return_data.html'
    message = None
    replacement_helper = ReplacementHelper()
    replacement_plots = Plot.objects.filter(selected=2, replaces=None)
    first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
    survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
    if not replacement_plots:
        message = 'No plots available to replace with.'
        return render_to_response(
                template, {
                    'message': message,
                    },
                    context_instance=RequestContext(request)
                )
    else:
        replacement_plots = []
        replacement_households = replacement_helper.replaceable_households(survey)
        replacement_plots = replacement_helper.replaceable_plots()
        if replaceble_plots and replacement_households:
            replacement_items = replacement_helper.replace_plot(replaceble_plots) + replacement_helper.replace_household(replacement_households)
        elif replaceble_plots and not replacement_households:
            replacement_items = replacement_helper.replace_plot(replaceble_plots)
        elif not replaceble_plots and replacement_households:
            replacement_items = replacement_helper.replace_household(replacement_households)
#             if not plot.is_dispatched:
#                 replaceble_items.append(replacing_plot.plot_identifier)
#                 replacement_count += 1
        plot_identifiers = []
        for plot in replacement_items:
            plot_identifiers.append(plot.plot_identifier)
        if plot_identifiers:
            pks = Plot.objects.filter(Q(**{'plot_identifier__in': plot_identifiers})).values_list('pk')
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
