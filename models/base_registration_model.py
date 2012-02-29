from django.db import models
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from base_registered_subject_model import BaseRegisteredSubjectModel

       
class BaseRegistrationModel (BaseRegisteredSubjectModel):

    #registered_subject = models.OneToOneField(RegisteredSubject,
    #    #editable=False  
    #    )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True
    
