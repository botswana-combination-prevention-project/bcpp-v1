from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp_list.models import FamilyPlanning
from bcpp.choices import YES_NO_DONT_ANSWER, WHERECIRC_CHOICE, ANCREG_CHOICE, PREGARV_CHOICE, YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class ReproductiveHealth (BaseScheduledVisitModel):
    
    """CS002"""
    
    numberchildren = models.IntegerField(
        verbose_name=("75. How many children have you given birth to? Please include any"
                      " children that may have died at (stillbirth) or after birth. "
                      "Do not include any current pregnancies or miscarriages that occur"
                      " early in pregnancy (prior to 20 weeks)."),
        max_length = 2,
        default=0,
        help_text=("Note: If participant does not want to answer, please record 0. "
                   "If no children, skip questions 84-87."),
        )

    morechildren = models.CharField(
        verbose_name = "76. Do you wish to have a child now or in the future?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    wherecirc = models.CharField(
        verbose_name=("77. Is it possible that you could become pregnant? "
                      "[If no, please indicate reason why you cannot become pregnant]"),
        max_length = 15,
        choices = WHERECIRC_CHOICE,
        help_text="",
        )

    familyplanning = models.ManyToManyField(FamilyPlanning,
        verbose_name=("78. In the past 12 months, have you used any methods to prevent"
                      " pregnancy ?"),
        max_length = 25,
        help_text="check all that apply",
        )

    currentpregnant = models.CharField(
        verbose_name = "79. Are you currently pregnant?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    ancreg = models.CharField(
        verbose_name = "80. Have you registered for antenatal care?",
        max_length = 15,
        choices = ANCREG_CHOICE,
        help_text="",
        )

    lnmp = models.DateTimeField(
        verbose_name = "81. When was your last normal menstrual period?",
        max_length = 25,
        null=True,
        blank=True,
        help_text=("Note:If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, record -4."),
        )

    lastbirth = models.DateField(
        verbose_name = "82. When did you last (most recently) give birth?",
        max_length = 25,
        null=True,
        blank=True,
        help_text=("Note:Leave blank if participant does not want to respond. "
                   "If participant is unable to estimate date, record -4."),
        )

    anclastpregnancy = models.CharField(
        verbose_name = "83. During your last pregnancy (not current pregnancy) did you go for antenatal care?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    hivlastpregnancy = models.CharField(
        verbose_name = "84. During your last pregnancy (not current pregnancy) were you tested for HIV?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    pregARV = models.CharField(
        verbose_name = "85. Were you given antiretroviral medications to protect the baby?",
        max_length = 15,
        choices = PREGARV_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_reproductivehealth_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Reproductive Health"
        verbose_name_plural = "Reproductive Health"
