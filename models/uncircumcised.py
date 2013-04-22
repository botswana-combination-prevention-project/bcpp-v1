from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import REASONCIRC_CHOICE, YES_NO_UNSURE, CIRCUMCISION_DAY, CIRCUMCISION_WEEK, CIRCUMCISION_MONTH, FUTUREREASONSSMC_CHOICE, AWAREFREE_CHOICE, YES_NO_DONT_ANSWER
#from base_scheduled_visit_model import BaseScheduledVisitModel
from base_circumcision import BaseCircumcision


class Uncircumcised (BaseCircumcision):
    
    """CS002"""
    
    reasoncirc = models.CharField(
        verbose_name = "Supplemental MC3. What is the main reason that have you not yet been circumcised?",
        max_length = 15,
        choices = REASONCIRC_CHOICE,
        help_text="",
        )

    futurecirc = models.CharField(
        verbose_name = "73. Would you ever consider being circumcised in the future?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    circumcision_day = models.CharField(
        verbose_name = ("Supplemental MC4. In the future, is there a particular time of day that you"
                        " would prefer to be circumcised?"),
        max_length = 15,
        choices = CIRCUMCISION_DAY,
        help_text="",
        )

    circumcision_week = models.CharField(
        verbose_name = ("Supplemental MC5. In the future, is there a particular day of the week that"
                        " you would prefer to be circumcised?"),
        max_length = 15,
        choices = CIRCUMCISION_WEEK,
        help_text="",
        )

    circumcision_year = models.CharField(
        verbose_name = ("Supplemental MC6. In the future, is there a particular time of year that you"
                        " would prefer to be circumcised?"),
        max_length = 15,
        choices = CIRCUMCISION_MONTH,
        help_text="",
        )

    futurereasonsSMC = models.CharField(
        verbose_name = ("Supplemental MC7. Which of the following might increase your willingness to"
                        " be circumcised the most?"),
        max_length = 15,
        choices = FUTUREREASONSSMC_CHOICE,
        help_text="",
        )

    service_facilities = models.CharField(
        verbose_name = ("Supplemental MC8. Were you aware that circumcision services are provided "
                        "free of charge at most health facilities?"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    awarefree = models.CharField(
        verbose_name = ("Supplemental MC9. Where did you learn that circumcision services were "
                        "available free at most health facilities?"),
        max_length = 15,
        choices = AWAREFREE_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_uncircumcised_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Uncircumcised"
        verbose_name_plural = "Uncircumcised"
