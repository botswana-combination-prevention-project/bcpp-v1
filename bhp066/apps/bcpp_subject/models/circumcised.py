from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import PLACE_CIRC, WHYCIRC_CHOICE, TIME_UNIT_CHOICE

from .base_circumcision import BaseCircumcision


class Circumcised (BaseCircumcision):
    circ_date = models.DateField(
        verbose_name=_('When were you circumcised?'),
        null=True,
        blank=True,)

    when_circ = models.IntegerField(
        verbose_name=_("At what age were you circumcised?"),
        max_length=2,
        null=True,
        blank=True,
        help_text=_("Note:Leave blank if participant does not want to respond."))

    age_unit_circ = models.CharField(
        verbose_name=_("The unit of age of circumcision is?"),
        max_length=25,
        choices=TIME_UNIT_CHOICE,
        null=True,
        blank=True,
        help_text="",
    )

    where_circ = models.CharField(
        verbose_name=_("Where were you circumcised?"),
        max_length=45,
        choices=PLACE_CIRC,
        null=True,
        help_text="supplemental")

    where_circ_other = OtherCharField(
        null=True)

    why_circ = models.CharField(
        verbose_name=_("What was the main reason why you were circumcised?"),
        max_length=55,
        choices=WHYCIRC_CHOICE,
        null=True,
        help_text="supplemental")

    why_circ_other = OtherCharField(
        null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
