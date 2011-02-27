from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_visit.choices import VISIT_INTERVAL_UNITS


"""
List of valid visit codes and their name
"""
class VisitDefinition(MyBasicUuidModel):

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
    instruction = models.TextField(
        verbose_name="Instructions",
        max_length=255,
        blank=True
        )    
    time_point = models.IntegerField(
        verbose_name = "Time point",
        )
  
    time_point_unit = models.CharField(
        max_length=15,    
        verbose_name="Units for visit intervals (default is days)",
        choices=VISIT_INTERVAL_UNITS,
        )        
    time_point_window_period_pre = models.IntegerField(
        verbose_name="Pre-visit interval of window period",
        help_text="time interval from visit time point to beginning of visit window",
        )
    time_point_window_period_post = models.IntegerField(
        verbose_name="Post-visit interval of window period",
        help_text="time interval from visit time point to end of visit window",
        )
    
    def __unicode__(self):
        return '%s: %s' % (self.code, self.title)
    
    class Meta:
        ordering = ['time_point']  
