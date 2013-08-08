from django.db import models
from bhp_base_model.validators import datetime_not_future
from bhp_base_model.validators import datetime_not_before_study_start
from django.core.validators import MaxValueValidator, MinValueValidator
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from lab_panel.models import Panel
from bhp_common.choices import YES_NO
from base_scheduled_visit_model import BaseScheduledVisitModel


class BloodDraw (BaseScheduledVisitModel):

    """CS002 - used when blood is drawn
        (What is the blood draw to be collected here??)"""
        
    is_blood_drawn = models.CharField(
        verbose_name="Was blood drawn today?",
        choices=YES_NO,
        max_length=3,
        help_text="",
        )
    is_blood_drawn_other = OtherCharField(
        verbose_name="If blood was not drawn today, please explain why",
        null=True,
        )

    draw_date = models.DateTimeField(
        verbose_name="What is the date and time of the blood draw?",
        null=True,
        blank=True,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text="",
        )
    
    record_available = models.CharField(
        verbose_name="Is record of last CD4 count available?",
        max_length=3,
        choices=YES_NO,
        help_text="",
        )
    
    last_cd4_count = models.DecimalField(
        verbose_name="What is the value of the last 'CD4' test recorded?",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text="",
        )
    last_cd4_drawn_date = models.DateField(
        verbose_name="Date last 'CD4' test was run",
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if Panel.objects.filter(name='Participant blood draw'):
            self.panel = Panel.objects.get(name='Participant blood draw')
        else:
            raise ValueError("Participant blood draw save() cannot determine the panel. Searching Panel on \Participant blood draw\', is panel table populated?")
        super(BloodDraw, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        ordering = ['-created']
        verbose_name = "Research blood draw"
        verbose_name_plural = "Research blood draw"
        unique_together = (('subject_visit', 'report_datetime'), )
