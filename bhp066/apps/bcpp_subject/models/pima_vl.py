from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ImproperlyConfigured

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import datetime_not_future
from edc.choices.common import YES_NO, PIMA, PIMA_SETTING_VL

from .base_scheduled_visit_model import BaseScheduledVisitModel

from apps.bcpp_tracking.classes import TrackerHelper


class PimaVl (BaseScheduledVisitModel):

    pima_type = models.CharField(
        verbose_name=_("Type mobile or household setting"),
        choices=PIMA_SETTING_VL,
        max_length=150,
        help_text="",
        default=PIMA_SETTING_VL[0][0],
        )

    pima_today = models.CharField(
        verbose_name=_("Was a PIMA CD4 done today?"),
        choices=YES_NO,
        max_length=3,
        help_text="",
        )

    pima_today_other = models.CharField(
        verbose_name=_("If no PIMA CD4 today, please explain why"),
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True,
        )

    pima_today_other_other = OtherCharField()

    pima_id = models.CharField(
        verbose_name=_("PIMA CD4 machine ID?"),
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='PIMA ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    cd4_datetime = models.DateTimeField(
        verbose_name=_("PIMA CD4 Date and time"),
        validators=[datetime_not_future],
        null=True,
        blank=True,
        )

    cd4_value = models.DecimalField(
        verbose_name=_("PIMA CD4 count"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text="",
        )

    history = AuditTrail()

    def validate_pimavl_no(self):
        tracker = TrackerHelper().tracked_value
        if tracker.tracked_value >= tracker.value_limit:
            raise ImproperlyConfigured('Pima Vl records ({}), cannot be greater than {} for {}.'.format(tracker.tracked_value, tracker.value_limit, tracker.value_type))

    def save(self, *args, **kwargs):
        self.validate_pimavl_no()
        super(PimaVl, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "PIMA CD4 count VL"
        verbose_name_plural = "PIMA CD4 count VL"
