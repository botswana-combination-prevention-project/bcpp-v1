from django.db import models
from django.utils.translation import ugettext_lazy as _
from edc.audit.audit_trail import AuditTrail
from apps.bcpp.choices import YES_NO_UNSURE
from .base_scheduled_visit_model import BaseScheduledVisitModel


POS_NEG = (('POS', 'POS'), )
MOH_CLINICS = (('Clinic 1', 'Clinic 1'), )
REFERRAL_REASONS = (('Referral Reason 1', 'Referral Reason 1'), )


class SubjectReferral(BaseScheduledVisitModel):
    """Proposed forms to be partially completed if values not collected from somewhere else
    and handed to CDC."""
    hiv_status = models.CharField(
        max_length=10,
        choices=POS_NEG,
        editable=False,
        )

    cd4_result = models.DecimalField(
        editable=False)

    who_staging = models.IntegerField()

    is_wasting = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE,
        )

    tb = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE,
        )

    in_hospital = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE,
        )

    diahorrea = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE,
        )

    pneumonia = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE,
        )

    preferred_clinic = models.CharField(
        max_length=50,
        choices=MOH_CLINICS,
        )

    reason = models.CharField(
        verbose_name=_("Reason for referral"),
        max_length=25,
        choices=REFERRAL_REASONS,
        default='unknown',
        editable=False,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
