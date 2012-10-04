from django.db import models
from bhp_adverse.models import DeathCauseInfo, DeathCauseCategory, \
    DeathMedicalResponsibility, DeathReasonHospitalized
from bhp_base_model.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_base_model.validators import date_not_before_study_start, \
    date_not_future
from bhp_registration.models import BaseRegisteredSubjectModel


class BaseDeath(BaseRegisteredSubjectModel):

    death_date = models.DateField(
        verbose_name="1. Date of Death:",
        validators=[
            date_not_before_study_start,
            date_not_future,
            ],
        help_text="",
        )

    death_cause_info = models.ForeignKey(DeathCauseInfo,
        verbose_name="2. What is the primary source of cause of death information? (if multiple source of information, list one with the smallest number closest to the top of the list) ",
        help_text="",
        )

    death_cause_info_other = OtherCharField(
        verbose_name="2a. if other specify...",
        blank=True,
        null=True,
        )

    death_cause = models.TextField(
        max_length=1000,
        verbose_name="4. Describe the major cause of death(including pertinent autopsy information if available),starting with the first noticeable illness thought to be related to death,continuing to time of death. ",
        help_text="Note: Cardiac and pulmonary arrest are not major reasons and should not be used to describe major cause)"
        )

    death_cause_category = models.ForeignKey(DeathCauseCategory,
        verbose_name="4a. Based on the above description, what category best defines the major cause of death? ",
        help_text="",
        )

    death_cause_other = OtherCharField(
        verbose_name="4b. if other specify...",
        blank=True,
        null=True,
        )

    death_medical_responsibility = models.ForeignKey(
        DeathMedicalResponsibility,
        verbose_name="5. Who was responsible for primary medical care of the participant during the month prior to death?",
        help_text="")

    participant_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="6. Was the participant hospitalised before death?",
        help_text="",
        )

    death_reason_hospitalized = models.ForeignKey(DeathReasonHospitalized,
        verbose_name="6a. if yes, hospitalized, what was the primary reason for hospitalisation? ",
        help_text="",
        blank=True,
        null=True,
        )

    days_hospitalized = models.IntegerField(
        verbose_name="6b. if yes, hospitalized, for how many days was the participant hospitalised during the illness immediately before death? ",
        help_text="",
        default=0,
        )

    class Meta:
        abstract = True
