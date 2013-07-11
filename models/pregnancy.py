from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp_list.models import FamilyPlanning
from bcpp.choices import YES_NO_DONT_ANSWER, WHERECIRC_CHOICE, ANCREG_CHOICE, PREGARV_CHOICE, YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Pregnancy (BaseScheduledVisitModel):

    """CS002"""

    more_children = models.CharField(
        verbose_name="76. Do you wish to have a child now or in the future?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    where_circ = models.CharField(
        verbose_name=("77. Is it possible that you could become pregnant? "
                      "[If no, please indicate reason why you cannot become pregnant]"),
        max_length=70,
        choices=WHERECIRC_CHOICE,
        help_text="",
        )

    family_planning = models.ManyToManyField(FamilyPlanning,
        verbose_name=("78. In the past 12 months, have you used any methods to prevent"
                      " pregnancy ?"),
        help_text="check all that apply",
        )
    family_planning_other = OtherCharField()

    current_pregnant = models.CharField(
        verbose_name="79. Are you currently pregnant?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    anc_reg = models.CharField(
        verbose_name="80. Have you registered for antenatal care?",
        max_length=55,
        null=True,
        blank=True,
        choices=ANCREG_CHOICE,
        help_text="",
        )

    lnmp = models.DateField(
        verbose_name="81. When was your last normal menstrual period?",
        help_text="",
        )

    last_birth = models.DateField(
        verbose_name="82. When did you last (most recently) give birth?",
        help_text="",
        )

    anc_last_pregnancy = models.CharField(
        verbose_name="83. During your last pregnancy (not current pregnancy) did you go for antenatal care?",
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    hiv_last_pregnancy = models.CharField(
        verbose_name="84. During your last pregnancy (not current pregnancy) were you tested for HIV?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="If respondent was aware that she was HIV-positive prior to last pregnancy",
        )

    preg_arv = models.CharField(
        verbose_name="85. Were you given antiretroviral medications to protect the baby?",
        max_length=95,
        choices=PREGARV_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_pregnancy_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
