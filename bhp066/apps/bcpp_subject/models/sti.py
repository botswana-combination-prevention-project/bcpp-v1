from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from bhp066.apps.bcpp_list.models import StiIllnesses

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Sti (BaseScheduledVisitModel):

    """A model completed by the user to record any potentially
    HIV-related illness in the past 12 months."""

    CONSENT_MODEL = SubjectConsent

    sti_dx = models.ManyToManyField(
        StiIllnesses,
        verbose_name="[Interviewer:] Indicate each potentially HIV-related illness that is reported"
                     " by the participant and/or recorded in his or her medical records",
        help_text="(tick all that apply)",
    )
    sti_dx_other = OtherCharField()

    wasting_date = models.DateField(
        verbose_name='wasting diagnosis date',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )
    diarrhoea_date = models.DateField(
        verbose_name='Diarrhoea diagnosis date',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )
    yeast_infection_date = models.DateField(
        verbose_name='Yeast Infection diagnosis date',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )
    pneumonia_date = models.DateField(
        verbose_name='Pneumonia diagnosis date',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )
    pcp_date = models.DateField(
        verbose_name='Date diagnosed with PCP',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )
    herpes_date = models.DateField(
        verbose_name='Date diagnosed with herpes',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If participant has a record, provide the details on the card. If no card, provide verbal response.",
    )

    comments = models.CharField(
        verbose_name="Comments",
        max_length=250,
        null=True,
        blank=True,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Potentially HIV-related illnesses"
        verbose_name_plural = "Potentially HIV-related illnesses"
