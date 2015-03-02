from django.db import models

from edc.core.identifier.models import BaseIdentifierModel


class HouseholdIdentifierHistory(BaseIdentifierModel):
    """A system model to track allocated household identifiers."""

    plot_identifier = models.CharField(max_length=25)

    household_sequence = models.IntegerField()

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_household"
