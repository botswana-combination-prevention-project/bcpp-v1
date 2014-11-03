from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from south.migration import base

from .base_clinic_visit_model import BaseClinicVisitModel

from .clinic_visit import ClinicVisit

from apps.clinic.choices import YES_NO_DWTA

from edc.audit.audit_trail import AuditTrail
from edc.entry_meta_data.managers import EntryMetaDataManager


class Questionnaire (BaseClinicVisitModel):

#     other_identifiers = models.CharField(
#         verbose_name=_("Does the participant have one of these identification numbers?"),
#         max_length=25,
#         choices=OTHER_IDENTIFIERS,
#         help_text="",
#         )
#
#     htc_and_or_pims = models.CharField(
#         verbose_name=_("Enter the HTC and or PIMS identifiers(comma separated)?"),
#         max_length=50,
#         null=True,
#         blank=True,
#         help_text="htc_identifier, pims_identifier",
#         )

    on_arv = models.CharField(
        verbose_name=_("Are you currently taking antiretroviral therapy (ARVs)?"),
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
        )

    knows_last_cd4 = models.CharField(
        verbose_name=_("Do you know the value of your last 'CD4' result?"),
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
        verbose_name = "Questionnaire"
        verbose_name_plural = "Questionnaire"
