from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.entry_meta_data.managers import EntryMetaDataManager

from apps.bcpp.choices import YES_NO_DWTA

from .base_clinic_visit_model import BaseClinicVisitModel
from .clinic_visit import ClinicVisit


class ClinicMain (BaseClinicVisitModel):

    pims_id = models.CharField(
        verbose_name="PIMS Identifier",
        max_length=15,
        null=True,
        blank=True,
        help_text="",
        )

    htc_id = models.CharField(
        verbose_name="HTC Identifier",
        max_length=12,
        null=True,
        blank=True,
        help_text="00-00-000-00",
        )

    on_arv = models.CharField(
        verbose_name=_("Are you currently taking antiretroviral therapy (ARVs)?"),
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
        )

    cd4_count = models.DecimalField(
        verbose_name=_("What is the value of your last 'CD4' test?"),
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(ClinicVisit)

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Main"
        verbose_name_plural = "Clinic Main"
