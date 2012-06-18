from django.db import models
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from registered_subject import RegisteredSubject

"""DO NOT USE THESE"""


class BaseRegisteredSubjectRegistrationModel (BaseUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject,
        editable=False  
        )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True

   
