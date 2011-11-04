from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_appointment.models import Appointment
from bhp_entry.models import ScheduledEntryBucket, AdditionalEntryBucket
from registered_subject import RegisteredSubject

        
class BaseRegisteredSubjectModel (MyBasicUuidModel):

    """ Base model for models that need a key to RegisteredSubject. Such
    models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments. Other instances may be Additional
    forms which are link to a subject but not a time point (for example, 
    a Death model or OffStudy model (see also AdditionalEntryBucket) 
    
    Use this along with BaseRegisteredSubjectModelAdmin()
    
    """

    registered_subject = models.OneToOneField(RegisteredSubject,
        #editable=False  
        )
    
    #report_datetime = models.DateTimeField("Today's date",
    #    validators=[
    #        datetime_not_before_study_start,
    #        datetime_not_future,],
    #    default = datetime.today(),
    #    )            
    
    
    def save(self, *args, **kwargs):

        super(BaseRegisteredSubjectModel, self).save(*args, **kwargs)

        # create appointments, (if model is in schedule_group)
        # this has been moved here from the admin save_model() method as the
        # create_appointments() method needs to access the saved model
        # for the base_appt_datetime, see Appointment.objects.create_appointments()
        Appointment.objects.create_appointments( 
            registered_subject = self.registered_subject, 
            model_name = self.__class__.__name__.lower(),
            )
        
        AdditionalEntryBucket.objects.update_status(
            registered_subject = self.registered_subject,    
            model_instance = self,
            )


    class Meta:
        abstract=True



