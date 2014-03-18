from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO
from edc.core.crypto_fields.fields import (EncryptedTextField, EncryptedDecimalField)
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..classes import HouseholdIdentifier
from ..managers import HouseholdManager
from ..choices import NOT_ENUMERATED_REASONS
from .plot import Plot


class ReplacementHistory(BaseDispatchSyncUuidModel):

    replacing_item = models.CharField(
        verbose_name='Item identifier used to replace another item',
        max_length=25,
        null=True,
        editable=False,
        )

    replaced_item = models.CharField(
        verbose_name='Item identifier of an item being replaced',
        max_length=25,
        null=True,
        editable=False,
        )

    replacement_datetime = models.DateTimeField(
        verbose_name='Report Date/Time',
        null=True,
        )

    replacement_reason = models.CharField(
        verbose_name='Reason for replacement',
        max_length=25,
        help_text=_("Reasons could be absentees, refusals, e.t.c"),
        null=True,
        editable=False,
        )

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-replacing_item', ]
