from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.choices.common import DEATH_RELATIONSIP_TO_STUDY
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_before_study_start, date_not_future
from edc.subject.adverse_event.models import DeathCauseInfo, DeathCauseCategory, DeathMedicalResponsibility

from bhp066.apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


class SubjectDeath(BaseMemberStatusModel):

    death_date = models.DateField(
        verbose_name="Date of Death:",
        validators=[
            date_not_before_study_start,
            date_not_future],
        help_text="",
    )

    site_aware_date = models.DateField(
        verbose_name="Date site aware of Death:",
        validators=[
            date_not_before_study_start,
            date_not_future],
        help_text="",
    )

    death_cause_info = models.ForeignKey(
        DeathCauseInfo,
        verbose_name=("What is the primary source of cause of death information? "
                      "(if multiple source of information, list one with the smallest "
                      "number closest to the top of the list) "),
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

    death_cause_category = models.ForeignKey(
        DeathCauseCategory,
        verbose_name="Based on the above description, what category best defines the major cause of death? ",
        help_text="",
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

    primary_medical_care_giver = models.ForeignKey(
        DeathMedicalResponsibility,
        verbose_name="Who was responsible for primary medical care during the month prior to death?",
        help_text="",
    )

    relationship_death_study = models.CharField(
        verbose_name="What is the relationship of the death to study participation?",
        max_length=50,
        choices=DEATH_RELATIONSIP_TO_STUDY,
        help_text="",
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.household_structure.household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(
                self.subject_undecided.household_member.household_structure.household.household_identifier))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectDeath, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.registered_subject)

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Subject Death"
        verbose_name_plural = "Subject Death"
