from datetime import datetime, date
from django.db import models
from lis.specimen.lab_result.models import BaseResult
from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite
from edc.base.model.fields import InitialsField
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.core.crypto_fields.fields import EncryptedCharField

from apps.bcpp_household.models import Plot

from ..managers import ViralLoadResultManager
from ..models import SubjectVisit


class ViralLoadResult(BaseDispatchSyncUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)
    subject_visit = subject_visit = models.ForeignKey(SubjectVisit)
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
    report_datetime = models.DateTimeField(
        verbose_name='Datetime result was reported',
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

    objects = models.Manager()#ViralLoadResultManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.sample_id, )

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'subject_visit__household_member__household_structure__household__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Viral Load Result"
        verbose_name_plural = "Viral Load Result"
