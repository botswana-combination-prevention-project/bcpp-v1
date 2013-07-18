from django.db import models
from django.core.urlresolvers import reverse
from bhp_base_model.validators import datetime_not_future
from bhp_base_model.validators import datetime_not_before_study_start
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from lab_panel.models import Panel
from bhp_common.choices import YES_NO
from base_scheduled_visit_model import BaseScheduledVisitModel


class BloodDraw (BaseScheduledVisitModel):
    
    """CS002 - used when blood is drawn
        (What is the blood draw to be collected here??)"""
    
    draw_date = models.DateTimeField(
        verbose_name="What is the date and time of the blood draw?",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text="",
        )
    
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
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_blooddraw_change', args=(self.id,))
    
    
    def save(self, *args, **kwargs):
        if Panel.objects.filter(name='Participant blood draw'):
            self.panel = Panel.objects.get(name='Participant blood draw')
        else:
            raise ValueError("Participant blood draw save() cannot determine the panel. Searching Panel on \Participant blood draw\', is panel table populated?")
        super(BloodDraw, self).save(*args, **kwargs)


    class Meta:
        app_label = 'bcpp_subject'
        ordering = ['-created']
        verbose_name = "Participant blood draw"
        verbose_name_plural = "Participant blood draw"
        unique_together = (('subject_visit', 'report_datetime'), )
