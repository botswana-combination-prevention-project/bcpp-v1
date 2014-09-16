import itertools

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.device.sync.exceptions import PendingTransactionError

from ..helpers import ReplacementHelper
from ..models import Plot


def replace_household_plot(request):
    template = 'replace_household_plot.html'
    if not Plot.objects.filter(selected=2, replaces=None).exists():
        return render_to_response(
            template, {'message': 'No plots available for replacement.'},
            context_instance=RequestContext(request)
            )
    else:
        producer_name = request.GET.get('producer_name')
        try:
            content_type_pk = None
            selected = []
            replacement_helper = ReplacementHelper()
            replaceables = replacement_helper.replace_plot(producer_name) + replacement_helper.replace_household(producer_name)
            # A plot that has been used to replace a plot or household and
            # not dispatched is added to the list of plots to be dispatched
            if replaceables:
                plot_identifiers = [plot.plot_identifier for plot in replaceables]
                for plot in Plot.objects.filter(selected=2, replaces__isnull=False).exclude(plot_identifier__in=plot_identifiers):
                    if not plot.is_dispatched:
                        plot_identifiers.append(plot.plot_identifier)
                pks = Plot.objects.filter(plot_identifier__in=plot_identifiers).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type_pk = ContentType.objects.get_for_model(Plot).pk
            return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type_pk, ",".join(selected)))
        except PendingTransactionError:
            return render_to_response(
                template, {'message': "Pending outgoing transaction on {}.".format(producer_name)},
                context_instance=RequestContext(request)
                )
