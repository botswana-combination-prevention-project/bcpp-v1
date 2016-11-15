from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_identifier.model_mixins import IdentifierModelMixin


class HouseholdIdentifierHistoryManager(models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class HouseholdIdentifierHistory(IdentifierModelMixin, BaseUuidModel):
    """A system model to track allocated household identifiers."""

    plot_identifier = models.CharField(max_length=25)

    household_sequence = models.IntegerField()

    objects = HouseholdIdentifierHistoryManager()

    history = HistoricalRecords()

    class Meta:
        app_label = "bcpp_household"
