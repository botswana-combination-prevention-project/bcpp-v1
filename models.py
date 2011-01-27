from django.db import models
from bhp_validators.validators import datetime_not_before_study_start, datetime_not_future,datetime_is_future, datetime_is_after_consent

class Af002SourceInfo (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  

class Af002InfantInfo (MyBasicListModel):
    class Meta:
        ordering = ['display_index']         

class Af002ReasonVisit (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   

class Af002 (MyBasicUuidModel):
    visit_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,],
        )

    visit_code = models.DecimalField(
        verbose_name="Visit Code",
        max_digits=5,
        decimal_places=1,
        validators = [
            RegexValidator("^[0-9]{4}\.[0-9]{1}$", "Ensure visit code uses format 9999.9"),
            ]
        )

    source_info = models.ForeignKey(Af002SourceInfo,
        verbose_name="1. What is the main source of this information?",
        help_text="",
        )
    source_info_other = OtherCharField(
        verbose_name="1a. if other specify...",
        blank=True,
        null=True,     
        )   
    reason_visit = models.ForeignKey(Af002ReasonVisit, 
        verbose_name="4. What is the reason for this visit?  ",
        help_text="",
        )  
    reason_missed = models.CharField(
        max_length=35,
        verbose_name="4a. If 'missed' above, Reason scheduled visit was missed",
        blank=True,
        null=True,   
        )  
    comments = models.TextField(
        max_length=250,
        verbose_name="5. Comment if any additional pertinent information about the participant",
        blank=True,
        null=True,   
        )    

    class Meta:
        abstract=True
