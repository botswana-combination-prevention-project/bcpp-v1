from django.db import models
from bhp_common.models import  MyBasicUuidModel
from bhp_visit.choices import VISIT_INTERVAL_UNITS

class BaseWindowPeriodItem(MyBasicUuidModel):

    """Base Model of fields that define a window period, either for visits or forms."""

    time_point = models.IntegerField(
        verbose_name = "Time point",
        default = 0,
        )
  
    base_interval = models.IntegerField(
        verbose_name = "Base interval",
        help_text = 'Interval from base timepoint 0 as an integer.',
        default = 0,        
        )
    
    base_interval_unit = models.CharField(
        max_length=10,    
        verbose_name="Base interval unit",
        choices=VISIT_INTERVAL_UNITS,
        default = 'D'
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

    grouping = models.CharField(
        verbose_name = 'Grouping',
        max_length = 25,
        null = True,
        blank = True,
        )

    class Meta:
        abstract = True
