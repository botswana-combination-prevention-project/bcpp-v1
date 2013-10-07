from django.db import models
from edc.base.model.validators import datetime_not_future
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from apps.bcpp.choices import (YES_NO_DONT_ANSWER, WHYNOARV_CHOICE, ADHERENCE4DAY_CHOICE, 
                               ADHERENCE4WK_CHOICE, NO_MEDICAL_CARE, WHYARVSTOP_CHOICE, 
                               YES_NO)
from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivCareAdherence (BaseScheduledVisitModel):

    """CS002-
    Note to Interviewer: This section is only to be completed by HIV-positive"
    " participants who knew that they were HIV-positive before today."""

    first_positive = models.DateField(
        verbose_name=_("When was your first positive HIV test result?"),
        validators = [datetime_not_future], 
        null=True,
        blank=True,
        help_text=("Note: If participant does not want to answer, leave blank. "
                   "If participant is unable to estimate date, leave blank."),
        )

    medical_care = models.CharField(
        verbose_name=_("Have you ever received HIV-related medical or clinical"
                      " care, for such things as a CD4 count (masole), IDCC/ PMTCT"
                      " registration, additional clinic-based counseling?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="if 'YES', answer HIV medical care section",
        )

    no_medical_care = models.CharField(
        verbose_name=_("What is the main reason you have not received HIV-related"
                       " medical or clinical care?"),
        max_length=70,
        null=True,
        blank=True,
        choices=NO_MEDICAL_CARE,
        help_text="",
        )

    ever_recommended_arv = models.CharField(
        verbose_name=_("Have you ever been recommended by a doctor/nurse or other healthcare "
                        "worker to start antiretroviral therapy (ARVs), a combination of medicines "
                        "to treat your HIV infection? [common medicines include: combivir, truvada, "
                        "atripla, nevirapine]"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        null=True,
        blank=True,
        help_text="",
        )

    arv_naive = models.CharField(
        verbose_name=_("Have you ever taken any antiretroviral therapy (ARVs) for your HIV infection?"
                        " [For women: Do not include treatment that you took during pregnancy to protect "
                        "your baby from HIV]"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    why_no_arv = models.CharField(
        verbose_name=_("What was the main reason why you have not started ARVs?"),
        max_length=75,
        null=True,
        blank=True,
        choices=WHYNOARV_CHOICE,
        help_text="",
        )
    why_no_arv_other = OtherCharField()

    first_arv = models.DateField(
        verbose_name=_("When did you first start taking antiretroviral therapy (ARVs)?"),
        validators = [datetime_not_future], 
        null=True,
        blank=True,
        help_text=("Note: If participant does not want to answer,leave blank.  "
                   "If participant is unable to estimate date, leave blank."),
        )

    on_arv = models.CharField(
        verbose_name=_("Are you currently taking antiretroviral therapy (ARVs)?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )
    arv_stop_date = models.DateField(
        verbose_name=_("When did you stop taking ARV\'s?"),
        validators = [datetime_not_future], 
        null=True,
        blank=True,
        help_text="",
        )

    arv_stop = models.CharField(
        verbose_name=_("What was the main reason why you stopped taking ARVs?"),
        max_length=80,
        choices=WHYARVSTOP_CHOICE,
        null=True,
        blank=True,
        help_text="",
        )
    arv_stop_other = OtherCharField()

    adherence_4_day = models.CharField(
        verbose_name=_("During the past 4 days, on how many days have you missed taking all your"
                        " doses of antiretroviral therapy (ART)?"),
        max_length=25,
        choices=ADHERENCE4DAY_CHOICE,
        null=True,
        blank=True,
        help_text="",
        )

    adherence_4_wk = models.CharField(
        verbose_name=_("Thinking about the past 4 weeks, on average, how would you rate your "
                        "ability to take all your medications as prescribed?"),
        max_length=25,
        null=True,
        blank=True,
        choices=ADHERENCE4WK_CHOICE,
        help_text="",
        )
    
    therapy_evidence = models.CharField(
        verbose_name=_("Is there evidence [OPD card, tablets, masa number] that the participant is on therapy?"),
        choices=YES_NO, 
        null=True,
        blank=True,
        max_length=3,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV care & Adherence"
        verbose_name_plural = "HIV care & Adherence"
