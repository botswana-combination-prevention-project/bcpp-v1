from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from registered_subject import RegisteredSubject

"""RATHER NOT USE THESE"""


class BaseRegisteredSubjectRegistrationModel (MyBasicUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject,
        editable=False  
        )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True


class BaseRegistrationForm(BaseRegisteredSubjectRegistrationModel):
    
    pass
        
        
    
