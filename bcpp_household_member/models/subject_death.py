from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future
from edc_constants.choices import DEATH_RELATIONSIP_TO_STUDY

from ..managers import HouseholdMemberManager

from .model_mixins import HouseholdMemberModelMixin


class SubjectDeath(HouseholdMemberModelMixin):

    """A model completed by the user to report the death of a participant."""

    death_date = models.DateField(
        verbose_name="Date of Death:",
        validators=[
            date_not_future],
        help_text="",
    )

    site_aware_date = models.DateField(
        verbose_name="Date site aware of Death:",
        validators=[
            date_not_future],
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
        verbose_name="Describe the major cause of death(including pertinent autopsy information if available),"
        "starting with the first noticeable illness thought to be related to death,continuing to time of death. ",
        help_text="Note: Cardiac and pulmonary arrest are not major reasons and should not be used to describe"
        " major cause)"
    )

    death_cause_other = OtherCharField(
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    duration_of_illness = models.IntegerField(
        verbose_name="Duration of acute illness directly causing death (in days, or choose Unknown)?",
        help_text="in days",
        default=0,
    )

    relationship_death_study = models.CharField(
        verbose_name="What is the relationship of the death to study participation?",
        max_length=50,
        choices=DEATH_RELATIONSIP_TO_STUDY,
        help_text="",
    )

    history = HistoricalRecords()

    objects = HouseholdMemberManager()

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectDeath, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.registered_subject)

    class Meta(HouseholdMemberModelMixin.Meta):
        app_label = "bcpp_household_member"
        verbose_name = "Subject Death"
        verbose_name_plural = "Subject Death"
