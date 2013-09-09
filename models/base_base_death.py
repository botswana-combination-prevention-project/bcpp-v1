from datetime import datetime
from django.db import models
from bhp_base_model.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_base_model.validators import date_not_before_study_start, date_not_future
from bhp_registration.models import BaseRegisteredSubjectModel
from bhp_adverse.managers import DeathManager
from death_list import DeathCauseInfo, DeathCauseCategory, DeathReasonHospitalized


class BaseBaseDeath(BaseRegisteredSubjectModel):

    death_date = models.DateField(
        verbose_name="Date of Death:",
        validators=[
            date_not_before_study_start,
            date_not_future,
            ],
        help_text="",
        )

    death_cause_info = models.ForeignKey(DeathCauseInfo,
        verbose_name="What is the primary source of cause of death information? (if multiple source of information, list one with the smallest number closest to the top of the list) ",
        help_text="",
        )

    death_cause_info_other = OtherCharField(
        verbose_name="if other specify...",
        blank=True,
        null=True,
        )

    death_cause = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Describe the major cause of death(including pertinent autopsy information if available),starting with the first noticeable illness thought to be related to death,continuing to time of death. ",
        help_text="Note: Cardiac and pulmonary arrest are not major reasons and should not be used to describe major cause)"
        )

    death_cause_category = models.ForeignKey(DeathCauseCategory,
        verbose_name="Based on the above description, what category best defines the major cause of death? ",
        help_text="",
        )

    death_cause_other = OtherCharField(
        verbose_name="if other specify...",
        blank=True,
        null=True,
        )

    participant_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was the participant hospitalised before death?",
        help_text="",
        )

    death_reason_hospitalized = models.ForeignKey(DeathReasonHospitalized,
        verbose_name="if yes, hospitalized, what was the primary reason for hospitalisation? ",
        help_text="",
        blank=True,
        null=True,
        )

    days_hospitalized = models.IntegerField(
        verbose_name="For how many days was the participant hospitalised during the illness immediately before death? ",
        help_text="",
        default=0,
        )

    comment = models.TextField(
        max_length=500,
        verbose_name="Comments",
        blank=True,
        null=True,
        )

    objects = DeathManager()

    def natural_key(self):
        return (self.death_date, ) + self.registered_subject.natural_key()

    def get_report_datetime(self):
        return datetime(self.death_date.year, self.death_date.month, self.death_date.day)

    class Meta:
        abstract = True
