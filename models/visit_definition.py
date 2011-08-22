from datetime import datetime, timedelta
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from bhp_common.models import  MyBasicUuidModel
from bhp_visit.utils import get_lower_window_days, get_upper_window_days
from bhp_visit.models import ScheduleGroup
from bhp_visit.models import BaseWindowPeriodItem

class VisitDefinition(BaseWindowPeriodItem):

    """Model to define a visit code, title, windows, schedule_group, etc."""

    code = models.CharField(
        max_length=4,
        validators = [MinLengthValidator(4),]        
        )        

    title = models.CharField(
        verbose_name="Title",
        max_length=35,
        )

    schedule_group = models.ManyToManyField(ScheduleGroup)

    instruction = models.TextField(
        verbose_name="Instructions",
        max_length=255,
        blank=True
        )    


    def get_lower_window_datetime(self, appt_datetime):
        days = get_lower_window_days(self.lower_window, self.lower_window_unit)
        td = timedelta(days=days)
        return appt_datetime - td
        
    def get_upper_window_datetime(self, appt_datetime):
        days = get_upper_window_days(self.upper_window, self.upper_window_unit)
        td = timedelta(days=days)
        return appt_datetime + td

    def __unicode__(self):
        return '{0}: {1}'.format(self.code, self.title)

    def get_absolute_url(self):
        return reverse('admin:bhp_visit_visitdefinition_change', args=(self.id,)) 

    class Meta:
        ordering = ['code', 'time_point']  
        app_label = "bhp_visit"
        db_table = 'bhp_form_visitdefinition'
