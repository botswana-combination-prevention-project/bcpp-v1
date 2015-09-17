from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.constants import CLOSED, OPEN, NEW
from edc.device.sync.models import BaseSyncUuidModel

from ..models import HouseholdStructure


class FollowUpList(BaseSyncUuidModel):

    household_structure = models.ForeignKey(HouseholdStructure)

    community = models.CharField(
        max_length=50)

    attempts = models.IntegerField(
        default=0)

    outcome = models.TextField(
        max_length=150,
    )

    status = models.CharField(
        max_length=15,
        choices=(
            (NEW, 'New'),
            (OPEN, 'Open'),
            (CLOSED, 'Closed'),
        ),
        default=NEW,
    )

    label = models.CharField(
        max_length=25,
        null=True,
        help_text="label to group reasons for contact, e.g. T1 preparation"
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ['household_structure', 'label']
