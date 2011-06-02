from datetime import datetime, timedelta
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import  MyBasicUuidModel
from bhp_visit.choices import VISIT_INTERVAL_UNITS
from bhp_visit.utils import get_lower_window_days, get_upper_window_days
from bhp_visit.models import ScheduleGroup

class BaseWindowPeriodItem(MyBasicUuidModel):

    """Base Model of fields that define a window period, either for visits or forms."""

    time_point = models.IntegerField(
        verbose_name = "Time point",
        default = 0,
        )
  
    lower_window = models.IntegerField(
        verbose_name="Window lower bound",
        default = 0,        
        )

    lower_window_unit = models.CharField(
        max_length=10,    
        verbose_name="Lower bound units",
        choices=VISIT_INTERVAL_UNITS,
        default = 'D'
        )        

    upper_window = models.IntegerField(
        verbose_name="Window upper bound",
        default = 0,        
        )
    upper_window_unit = models.CharField(
        max_length=10,    
        verbose_name="Upper bound units",
        choices=VISIT_INTERVAL_UNITS,
        default = 'D'
        )        

    class Meta:
        abstract = True

class VisitDefinition(BaseWindowPeriodItem):

    """Model to define a visit code, title, windows, schedule_group, etc."""

    code = models.IntegerField(
        validators = [
            MinValueValidator(1000),
            MaxValueValidator(9999),
            ]
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
    
    """
    def get_lower_window_datetime(self, appt_datetime):
        days = get_lower_window_days(self.lower_window, self.lower_window_unit)
        td = timedelta(days=days)
        return appt_datetime - td
        
    def get_upper_window_datetime(self, appt_datetime):
        days = get_upper_window_days(self.upper_window, self.upper_window_unit)
        td = timedelta(days=days)
        return appt_datetime + td
    """
    def __unicode__(self):
        return '{0}: {1}'.format(self.code, self.title)
    
    class Meta:
        ordering = ['code', 'time_point']  
        app_label = 'bhp_visit'                    

