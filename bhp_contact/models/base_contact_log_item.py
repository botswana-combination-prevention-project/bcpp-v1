from django.db import models
from bhp_consent.models import BaseConsentedUuidModel
from bhp_common.choices import YES_NO
from bhp_crypto.fields import EncryptedTextField


class BaseContactLogItem(BaseConsentedUuidModel):

    """Detail model for "inline" of a Contact Log."""

    contact_datetime = models.DateTimeField(
        verbose_name='Date of call')

    is_contacted = models.CharField(
        verbose_name='Did someone answer?',
        max_length=10,
        choices=YES_NO,
        )

    information_provider = models.CharField(
        verbose_name="Who answered?",
        max_length=20,
        help_text="",
        null=True,
        blank=True,
        )

    comment = EncryptedTextField(
        max_length=100,
        blank=True,
        null=True,
        )

    class Meta:
        abstract = True
