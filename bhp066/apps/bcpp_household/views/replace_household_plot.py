import itertools

from django.contrib import messages
from django.db.models import get_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import OperationalError
from django.db.utils import ConnectionDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.device.sync.models import Producer
from edc.device.sync.exceptions import PendingTransactionError
from edc.device.sync.utils import getproducerbyaddr

from ..exceptions import ReplacementError
from ..helpers import ReplacementHelper
from ..models import Plot


@login_required
def replace_household_plot(request):
    template = 'replace_household_plot.html'
    NotebookPlotList = get_model('bcpp_household', 'notebookplotlist')
    if not Plot.objects.filter(selected=2, replaces=None).exists():
        messages.add_message(request, messages.INFO, 'There are no plots available for replacement.')
    else:
        producer_name = request.GET.get('producer_name')
        try:
            producer = Producer.objects.get(name=producer_name)
            getproducerbyaddr(producer)

            content_type_pk = None
            selected = []
            replacement_helper = ReplacementHelper()
            replaceables = list(replacement_helper.replace_plot(producer.settings_key))
            replaceables.extend(list(replacement_helper.replace_household(producer.settings_key)))
            # A plot that has been used to replace a plot or household and
            # not dispatched is added to the list of plots to be dispatched
            if replaceables:
                plot_identifiers = [plot.plot_identifier for plot in replaceables]
                for plot in Plot.objects.filter(plot_identifier__in=plot_identifiers):
                    if not plot.is_dispatched:
                        plot_identifiers.append(plot.plot_identifier)
                pks = Plot.objects.filter(plot_identifier__in=plot_identifiers).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type_pk = ContentType.objects.get_for_model(Plot).pk
                content_type2 = ContentType.objects.get_for_model(NotebookPlotList)
                if not NotebookPlotList.objects.using(producer_name).all():
                    return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&notebook_plot_list=not_allocated&items={1}".format(content_type_pk, ",".join(selected)))
                else:
                    return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}&notebook_plot_list=allocated&ct1={2}".format(content_type_pk, ",".join(selected), content_type2.pk))
        except Producer.DoesNotExist:
            messages.add_message(request, messages.ERROR, (
                '\'{}\' not a valid producer. See model Producer.').format(producer_name))
        except ConnectionDoesNotExist as connection_does_not_exist:
            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                   'Got {}'.format(producer.settings_key, str(connection_does_not_exist)))
        except OperationalError as operational_error:
            messages.add_message(request, messages.ERROR, (
                'Unable to connect to producer with settings key \'{}\'. '
                'Got {}').format(producer.settings_key, str(operational_error)))
        except PendingTransactionError as pending_transaction_error:
            messages.add_message(request, messages.ERROR, str(pending_transaction_error))
            # "Pending outgoing transaction on {}.".format(producer_name)
        except ReplacementError as replacement_error:
            messages.add_message(request, messages.ERROR, str(replacement_error))
    return render_to_response(
        template, {},
        context_instance=RequestContext(request)
    )
