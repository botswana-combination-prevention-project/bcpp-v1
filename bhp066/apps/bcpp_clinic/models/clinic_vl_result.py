from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import InitialsField
from edc.core.bhp_variables.models import StudySite
from edc.core.crypto_fields.fields import EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.entry_meta_data.managers import EntryMetaDataManager

from .base_clinic_visit_model import BaseClinicVisitModel
from ..models import ClinicVisit


class ClinicVLResult(BaseClinicVisitModel):

#     sample_id = models.CharField(
#         verbose_name='Sample Identifier',
#         max_length=25,
#         unique=True,
#         help_text="It could be an Aliquot identifier if applicable.")
    site = models.ForeignKey(StudySite)
    clinician_initials = InitialsField(
        verbose_name='Clinician initial',
        default='--',
        )
    collection_datetime = models.DateTimeField(
        verbose_name='The datetime sample was drawn',
        help_text='',
        )
#     received_datetime = models.DateTimeField(
#         verbose_name='The datetime sample was received',
#         help_text='',
#         )
#     test_datetime = models.DateTimeField(
#         verbose_name='Test datetime',
#         help_text='',
#         )
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
    validation_date = models.DateField(
        verbose_name='Date result was validated',
        help_text='',
        )
#     assay_performed_by = EncryptedCharField(
#         max_length=35,
#         verbose_name="Assay performed by",
#         )
    validated_by = EncryptedCharField(
        max_length=35,
        verbose_name="Validated by",
        )
#     validation_reference = models.CharField(
#         verbose_name='Validation reference',
#         max_length=25,
#         unique=True,
#         help_text="Validation reference",
#         )

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(ClinicVisit)

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic VL Result"
        verbose_name_plural = "Clinic VL Result"
