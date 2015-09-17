from django.db import models

from edc_base.model.models import BaseUuidModel


class Replaceable(BaseUuidModel):
    """A system model used to track and manage replaceable plots and households."""
    replaced = models.BooleanField(default=False)

    replaced_reason = models.CharField(max_length=25, null=True)

    producer_name = models.CharField(max_length=25, null=True)

    app_label = models.CharField(max_length=25)

    model_name = models.CharField(max_length=25)

    community = models.CharField(max_length=25)

    plot_status = models.CharField(max_length=25)

    item_pk = models.CharField(max_length=36)

    item_identifier = models.CharField(max_length=25)

    objects = models.Manager()

    class Meta:
        app_label = 'bcpp_household'
