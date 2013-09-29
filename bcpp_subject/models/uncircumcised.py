from django.db import models
from django.utils.translation import ugettext as _
from edc_core.audit_trail.audit import AuditTrail
from edc_core.bhp_base_model.fields import OtherCharField
from bcpp.choices import REASONCIRC_CHOICE, YES_NO_UNSURE, FUTUREREASONSSMC_CHOICE, AWAREFREE_CHOICE, YES_NO_DONT_ANSWER
from .base_circumcision import BaseCircumcision


class Uncircumcised (BaseCircumcision):

    reason_circ = models.CharField(
        verbose_name=_("What is the main reason that you have not yet been circumcised?"),
        max_length=65,
        null=True,
        choices=REASONCIRC_CHOICE,
        help_text="supplemental",
        )
    reason_circ_other = OtherCharField(
        null=True,)

    future_circ = models.CharField(
        verbose_name=_("Would you ever consider being circumcised in the future?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    future_reasons_smc = models.CharField(
        verbose_name=_("Which of the following might increase your willingness to"
                        " be circumcised the most?"),
        max_length=75,
        choices=FUTUREREASONSSMC_CHOICE,
        null=True,
        help_text="supplemental",
        )

    service_facilities = models.CharField(
        verbose_name=_("Were you aware that circumcision services are provided "
                        "free of charge at most health facilities?"),
        max_length=35,
        choices=YES_NO_DONT_ANSWER,
        null=True,
        help_text="supplemental",
        )

    aware_free = models.CharField(
        verbose_name=_("Where did you learn that circumcision services were "
                        "available free at most health facilities?"),
        max_length=85,
        null=True,
        blank=True,
        choices=AWAREFREE_CHOICE,
        help_text="supplemental",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Uncircumcised"
        verbose_name_plural = "Uncircumcised"
