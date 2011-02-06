from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from bhp_validators.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_future, datetime_is_after_consent
from choices import WINDOW_PERIOD_UNITS

"""
List of valid visit codes and their name
"""
class VisitDefinition(MyBasicListModel):
    code = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators = [
            RegexValidator("^[0-9]{4}\.[0-9]{1}$", "Ensure visit code uses format 9999.9"),
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
    visit_time_point = models.IntegerField(
        verbose_name = "Time point",
        )    
    visit_time_point_unit = models.CharField(
        verbose_name="Units for visit intervals (default is days)",
        choices=WINDOW_PERIOD_UNITS,
        )        
    window_period_pre = models.IntegerField(
        verbose_name="Pre-visit interval of window period",
        help_text="time interval from visit time point to beginning of visit window",
        )
    window_period_post = models.IntegerField(
        verbose_name="Post-visit interval of window period",
        help_text="time interval from visit time point to end of visit window",
        )
    window_period_post_unit = models.CharField(
        verbose_name="Units for Post-visit interval",
        choices=WINDOW_PERIOD_UNITS,
        )        
    
    class Meta:
        ordering = ['display_index']  

class VisitTrackingSourceInfo (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  

class VisitTrackingReasonVisit (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   

class VisitTracking (MyBasicUuidModel):

    visit_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )

    """visit_definition is the visit code plus other information"""    
    visit_definition = models.ForeignKey(VisitDefinition,
        verbose_name="Visit",
        help_text = "For tracking within the window period of a visit, use the decimal convention. Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)
        )

    """visit_instance should be populated by the system"""    
    visit_instance = models.IntegerField(
        verbose_name="Instance",
        validators=[
            IsNextVisitInstance,
            MinValueValidator(0),
            MaxValueValidator(9),
            ],
        read_only=True,    
        help_text="A decimal to represent an additional report to be included with the original visit report. (NNNN.0)",    
        )     
        
    source_info = models.ForeignKey(VisitTrackingSourceInfo,
        verbose_name="1. What is the main source of this information?",
        help_text="",
        )
        
    source_info_other = OtherCharField(
        verbose_name="1a. if other specify...",
        blank=True,
        null=True,     
        )   
        
    reason_visit = models.ForeignKey(VisitTrackingReasonVisit, 
        verbose_name="4. What is the reason for this visit?  ",
        help_text="",
        )  
        
    reason_missed = models.CharField(
        verbose_name="4a. If 'missed' above, Reason scheduled visit was missed",
        max_length=35,
        blank=True,
        null=True,   
        )  
        
    """
        this value should be suggested by the sytem by may be edited by the user.
        a further save check should confirm that the date makes sense relative
        to the visit schedule
    """    
    next_scheduled_visit_datetime = models.DateTimeField(
        verbose_name="Next scheduled visit date and time",
        validators=[
            datetime_is_after_consent,
            datetime_is_future,
            ],       
        
    comments = models.TextField(
        verbose_name="5. Comment if any additional pertinent information about the participant",
        max_length=250,
        blank=True,
        null=True,   
        )    

    class Meta:
        abstract=True
