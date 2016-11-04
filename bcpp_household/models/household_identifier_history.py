from django.db import models

from edc_identifier.models import BaseIdentifierModel
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel


class HouseholdIdentifierHistory(BaseIdentifierModel, SyncModelMixin, BaseUuidModel):
    """A system model to track allocated household identifiers."""

    plot_identifier = models.CharField(max_length=25)

    household_sequence = models.IntegerField()

    def ignore_for_dispatch(self):
        return True

    def deserialize_prep(self, **kwargs):
        # HouseholdIdentifierHistory being deleted by an IncommingTransaction, we go ahead and delete it.
        # An extra household created by mistake.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = "bcpp_household"
