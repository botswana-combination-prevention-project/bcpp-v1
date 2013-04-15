from datetime import datetime, time
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from bhp_base_model.validators import eligible_if_yes
from bhp_common.choices import YES_NO, YES_NO_UNSURE
from audit_trail.audit import AuditTrail
from bhp_adverse.models import BaseBaseDeath


class SubjectDeath(BaseBaseDeath):

    sufficient_records = models.CharField(
        verbose_name="1. Are sufficient records for the 30 days before death available for review? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO' STOP, not eligibile",
        )
    document_hiv = models.CharField(
        verbose_name="2. Does the record document that the decedent had HIV? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO' STOP, not eligibile",
        )
    document_community = models.CharField(
        verbose_name="3. Does the record document that the decedent lived one of the study communities? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO' STOP, not eligibile",
        )
    document_community_other = models.CharField(
        verbose_name="3b. If yes, record community",
        max_length=30,
        null=True, 
        blank=True,
        )
    death_year = models.DateField(
        verbose_name="4. What was the month and year of death?  ",
        help_text="if 'More than 6 months prior,' STOP, not eligible.",
        )
    decendent_death_age = models.IntegerField(
        verbose_name="5. What was the age in years of the decedent at the time of death? ",
        max_length=2,
        validators=[MinValueValidator(16), MaxValueValidator(64)],
        help_text="if 'Not 16-64 years,' STOP, not eligible.",
        )
    hospital_death = models.CharField(
        verbose_name="7. Did the decedent die in the hospital? ",
        max_length=3,
        choices=YES_NO,
        help_text="",
        )
    decedent_haart = models.CharField(
        verbose_name=("8. Was the decedent receiving antiretroviral therapy (HAART) during the 30 days"
                      " before his/her death? "),
        max_length=8,
        choices=YES_NO_UNSURE,
        help_text="if 'NO' SKIP to question 10",
        )
    decedent_haart_start = models.DateField(
        verbose_name="9. When did the decedent start antiretroviral therapy? ",
        null=True, 
        blank=True,
        help_text="",
        )
    decedent_hospitalized = models.CharField(
        verbose_name="10. Did resident spend at least one night in the hospital within 30 days of his/her death?",
        max_length=3,
        choices=YES_NO,
        help_text="if 'NO' SKIP to question 12",
        )
    days_decedent_hospitalized = models.IntegerField(
        verbose_name=("11.How many nights did the decedent spend in the hospital during the 30 days before"
                      " his/her death? "),
        null=True, 
        blank=True,
        help_text=("For hospitalization that begin prior to 30 days before death, only nights"
                   " within the 30 day window preceding death should be included"),
        )
    hospital_visits = models.IntegerField(
        verbose_name=("12. How many visits did the decedent make to the health post, clinic,"
                      " or hospital during the 30 days before his/her death? "),
        help_text=" if 'Zero,' END abstraction",
        )
    doctor_evaluation = models.IntegerField(
        verbose_name="13. How many of these visits included an evaluation or counselling by a doctor?",
        null=True, 
        blank=True,
        help_text="",
        )

    
    history = AuditTrail()

    def __unicode__(self):
        return '%s ' % (self.registered_subject)

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Death Economic Abstraction"
        verbose_name_plural = "Death Economic Abstraction"
