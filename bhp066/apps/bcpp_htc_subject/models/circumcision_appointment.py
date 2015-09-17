from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future
from apps.bcpp.choices import YES_NO
from .base_scheduled_model import BaseScheduledModel


class CircumcisionAppointment (BaseScheduledModel):

    circumcision_ap = models.CharField(
        verbose_name=_("Was a male circumcision appointment made?"),
        max_length=15,
        choices=YES_NO,
        help_text='If male, negative and uncircumcised',
        )

    circumcision_ap_date = models.DateField(
        verbose_name=_("Male circumcision appointment date"),
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=_("Format is YYYY-MM-DD (If male, negative and uncircumcised)"),
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Circumcision Appointment"
        verbose_name_plural = "Circumcision Appointment"
