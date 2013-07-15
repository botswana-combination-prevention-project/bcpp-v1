from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp.choices import REASONCIRC_CHOICE, YES_NO_UNSURE, CIRCUMCISION_DAY, CIRCUMCISION_WEEK, CIRCUMCISION_MONTH, FUTUREREASONSSMC_CHOICE, AWAREFREE_CHOICE, YES_NO_DONT_ANSWER


class Uncircumcised (BaseCircumcision):
    
    """CS002"""
    
    reason_circ = models.CharField(
        verbose_name="What is the main reason that you have not yet been circumcised?",
        max_length=15,
        null=True,
        choices=REASONCIRC_CHOICE,
        help_text="supplemental",
        )

    future_circ = models.CharField(
        verbose_name="Would you ever consider being circumcised in the future?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    circumcision_day = models.CharField(
        verbose_name=("In the future, is there a particular time of day that you"
                        " would prefer to be circumcised?"),
        max_length=15,
        choices=CIRCUMCISION_DAY,
        null=True,
        help_text="supplemental",
        )
    circumcision_day_other = OtherCharField(
        null=True,)

    circumcision_week = models.CharField(
        verbose_name=("In the future, is there a particular day of the week that"
                        " you would prefer to be circumcised?"),
        max_length=15,
        choices=CIRCUMCISION_WEEK,
        null=True,
        help_text="supplemental",
        )
    circumcision_week_other = OtherCharField(
        null=True,)

    circumcision_year = models.CharField(
        verbose_name=("In the future, is there a particular time of year that you"
                        " would prefer to be circumcised?"),
        max_length=15,
        choices=CIRCUMCISION_MONTH,
        null=True,
        help_text="supplemental",
        )
    circumcision_year_other = OtherCharField(
        null=True,)

    future_reasons_smc = models.CharField(
        verbose_name=("Which of the following might increase your willingness to"
                        " be circumcised the most?"),
        max_length=15,
        choices=FUTUREREASONSSMC_CHOICE,
        null=True,
        help_text="supplemental",
        )

    service_facilities = models.CharField(
        verbose_name=("Were you aware that circumcision services are provided "
                        "free of charge at most health facilities?"),
        max_length=15,
        choices=YES_NO_DONT_ANSWER,
        null=True,
        help_text="supplemental",
        )

    aware_free = models.CharField(
        verbose_name=("Where did you learn that circumcision services were "
                        "available free at most health facilities?"),
        max_length=15,
        null=True,
        blank=True,
        choices=AWAREFREE_CHOICE,
        help_text="supplemental",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_uncircumcised_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Uncircumcised"
        verbose_name_plural = "Uncircumcised"
