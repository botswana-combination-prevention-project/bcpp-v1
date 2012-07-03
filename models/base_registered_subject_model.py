from django.db import models
from django.db.models import get_app, get_models
from bhp_appointment.models import Appointment
from bhp_entry.models import AdditionalEntryBucket
from registered_subject import RegisteredSubject
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_visit_tracking.models.base_visit_tracking import BaseVisitTracking
 
        
class BaseRegisteredSubjectModel (BaseUuidModel):

    """ Base model for models that need a key to RegisteredSubject. Such
    models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments. Other instances may be Additional
    forms which are link to a subject but not a time point (for example, 
    a Death model or OffStudy model (see also AdditionalEntryBucket) 
    
    Use this along with BaseRegisteredSubjectModelAdmin()
    
    """
    registered_subject = models.OneToOneField(RegisteredSubject)            
    
    def get_visit_model(self, instance):
        for model in get_models(get_app(instance._meta.app_label)):
            if isinstance(model(), BaseVisitTracking):
                return model
        raise TypeError('Unable to determine the visit model from instance {0} for app {1}'.format(instance._meta.model_name, instance._meta.app_label))
        
    def save(self, *args, **kwargs):

        super(BaseRegisteredSubjectModel, self).save(*args, **kwargs)

        # create appointments, (if model is in schedule_group)
        # this has been moved here from the admin save_model() method as the
        # create_appointments() method needs to access the saved model
        # for the base_appt_datetime, see Appointment.objects.create_appointments()

        if not kwargs.get('suppress_autocreate_on_deserialize', False):
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





