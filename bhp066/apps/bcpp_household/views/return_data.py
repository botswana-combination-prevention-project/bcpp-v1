import itertools

from django.contrib.contenttypes.models import ContentType
from django.db.models import Min
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.bcpp_survey.models import Survey

from ..helpers import ReplacementHelper
from ..models import Plot, Household


def return_data(request):
    content_type = None
    replaceble_plots = []
    replacement_items = []
    replacing_plot = None
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
    elif request.GET.get('return_all'):
        replacement_plots = []
        replacement_households = replacement_helper.replaceable_households(survey)
        replacement_plots = replacement_helper.replaceable_plots()
        if replaceble_plots and replacement_households:
            replacement_items = replacement_helper.replace_plot(replaceble_plots) + replacement_helper.replace_household(replacement_households)
        elif replaceble_plots and not replacement_households:
            replacement_items = replacement_helper.replace_plot(replaceble_plots)
        elif not replaceble_plots and replacement_households:
            replacement_items = replacement_helper.replace_household(replacement_households)
        # A plot that has been used to replace a plot or household and not dispatched is added to the list of plots to be dispatched
        for plot in Plot.objects.filter(selected=2):
            if plot.producer_dispatched_to == 'Not Dispatched' and plot.replaces:
                if not plot in replacement_items:
                    replacement_items.append(plot)
        plot_identifiers = []
        for plot in replacement_items:
            plot_identifiers.append(plot.plot_identifier)
        if plot_identifiers:
            pks = Plot.objects.filter(Q(**{'plot_identifier__in': plot_identifiers})).values_list('pk')
            selected = list(itertools.chain(*pks))
            content_type = ContentType.objects.get_for_model(Plot)
            return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))

    elif request.GET.get('household_identifier'):
        household_identifier = request.GET.get('household_identifier')
        if replacement_plots and len(replacement_plots) > 1:
            replacing_plot = replacement_plots[0]
            if Household.objects.filter(household_identifier=household_identifier):
                household = Household.objects.get(household_identifier=household_identifier)
                replacement_items = replacement_helper.replace_household([household])
            if replacing_plot.producer_dispatched_to == 'Not Dispatched' and replacing_plot.replaces:
                if not plot in replacement_items:
                    replacement_items.append(plot)
        pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_items})).values_list('pk')
        selected = list(itertools.chain(*pks))
        content_type = ContentType.objects.get_for_model(Plot)
        return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
    elif request.GET.get('plot_identifier'):
        plot_identifier = request.GET.get('plot_identifier')
        if replacement_plots and len(replacement_plots) > 1:
            replacing_plot = replacement_plots[0]
            if Plot.objects.filter(plot_identifier=plot_identifier):
                plot = Plot.objects.get(plot_identifier=plot_identifier)
                replacement_items = replacement_helper.replace_household([plot])
            if replacing_plot.producer_dispatched_to == 'Not Dispatched' and replacing_plot.replaces:
                if not plot in replacement_items:
                    replacement_items.append(plot)
        pks = Plot.objects.filter(Q(**{'plot_identifier__in': replacement_items})).values_list('pk')
        selected = list(itertools.chain(*pks))
        content_type = ContentType.objects.get_for_model(Plot)
        return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
