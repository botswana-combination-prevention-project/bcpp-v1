from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.core.bhp_variables.models import StudySite
from edc.base.model.fields import InitialsField
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.core.crypto_fields.fields import EncryptedCharField

from ..managers import ViralLoadResultManager

from .base_scheduled_visit_model import BaseScheduledVisitModel


class ViralLoadResult(BaseScheduledVisitModel):

    sample_id = models.CharField(
        verbose_name='Aliquot Identifier',
        max_length=25,
        unique=True,
        help_text="Aliquot identifier",
        editable=False)

    clinic = models.ForeignKey(StudySite)

    clinician_initials = InitialsField(
        verbose_name='Clinician initial',
        default='--',
    )

    collection_datetime = models.DateTimeField(
        verbose_name='The datetime sample was drawn',
        help_text='',
    )

    received_datetime = models.DateTimeField(
        verbose_name='The datetime sample was received',
        help_text='',
    )

    test_datetime = models.DateTimeField(
        verbose_name='Test datetime',
        help_text='',
    )

    assay_date = models.DateField(
        verbose_name='Assay date',
        help_text='',
    )

    result_value = models.IntegerField(
        verbose_name="Result Value",
        help_text=("copies/ml"),)

    comment = EncryptedTextField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True
    )

    validation_datetime = models.DateTimeField(
        verbose_name='Datetime result was reported',
        help_text='',
    )

    assay_performed_by = EncryptedCharField(
        max_length=35,
        verbose_name="Assay performed by",
    )

    validated_by = EncryptedCharField(
        max_length=35,
        verbose_name="Validated by",
    )

    validation_reference = models.CharField(
        verbose_name='Validation reference',
        max_length=25,
        unique=True,
        help_text="Validation reference",
    )

    objects = ViralLoadResultManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.sample_id, )

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Viral Load Result"
        verbose_name_plural = "Viral Load Result"
