from django.db import models
from bhp_consent.models import BaseConsentedUuidModel
from bhp_common.choices import YES_NO
from bhp_crypto.fields import EncryptedCharField


class BaseContactLogItem(BaseConsentedUuidModel):

    contact_datetime = models.DateTimeField()

    contact_type = models.CharField(
        verbose_name="Contact type",
        max_length=20,
        help_text="",
        )

    is_contacted = models.CharField(
        verbose_name='Contacted?',
        max_length=10,
        choices=YES_NO,
        )

    information_provider = models.CharField(
        verbose_name="Person completing interview",
        max_length=20,
        help_text="",
        null=True,
        blank=True,
        )

    comment = EncryptedCharField(
        max_length=100,
        blank=True,
        null=True,
        )

    class Meta:
        abstract = True
