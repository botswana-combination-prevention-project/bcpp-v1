from __future__ import absolute_import

from bhp066.config.celery import app as celery_app

from ..helpers import ReplacementHelper
from ..models import Replaceable, Household, Plot


@celery_app.task
def update_replaceables(*args):
    """Updates the instances in Replaceables and returns the number of instances updated.

    Update is by deleting then creating."""

    Replaceable.objects.all().delete()
    Household.objects.all().update(replaceable=False)
    Household.objects.filter(replaced_by__isnull=False).update(replaceable=True)
    Plot.objects.all().update(replaceable=False)
    Plot.objects.filter(replaced_by__isnull=False).update(replaceable=True)
    for plot in Plot.objects.filter(replaceable=True):
        Replaceable.objects.create(
            replaced=True,
            replaced_reason='',
            app_label=plot._meta.app_label,
            model_name=plot._meta.object_name,
            community=plot.community,
            item_identifier=plot.plot_identifier,
            item_pk=plot.pk,
            plot_status=plot.status,
            producer_name=None)
    for household in Household.objects.filter(replaceable=True):
        Replaceable.objects.create(
            replaced=True,
            replaced_reason='',
            app_label=household._meta.app_label,
            model_name=household._meta.object_name,
            community=household.community,
            item_identifier=household.get_identifier(),
            item_pk=household.pk,
            plot_status=household.plot.status,
            producer_name=None)
    replacement_helper = ReplacementHelper()
    replaceables = list(replacement_helper.replaceable_households())
    replaceables.extend(replacement_helper.replaceable_plots())
    n = 0
    for replaceable, dispatch_item_register in replaceables:
        try:
            producer_name = dispatch_item_register.producer.name
        except AttributeError:
            producer_name = None
        try:
            plot_status = replaceable.plot.status
        except AttributeError:
            plot_status = replaceable.status
        Replaceable.objects.create(
            replaced=False,
            app_label=replaceable._meta.app_label,
            model_name=replaceable._meta.object_name,
            community=replaceable.community,
            item_identifier=replaceable.get_identifier(),
            item_pk=replaceable.pk,
            plot_status=plot_status,
            producer_name=producer_name)
        replaceable.replaceable = True
        replaceable.save_base(update_fields='replaceable')
        n += 1
    return n
