from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_appointment.models import Appointment
from bhp_entry.models import AdditionalEntryBucket
from registered_subject import RegisteredSubject

        
class BaseRegisteredSubjectModel (MyBasicUuidModel):

    """ Base model for models that need a key to RegisteredSubject. Such
    models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments. Other instances may be Additional
    forms which are link to a subject but not a time point (for example, 
    a Death model or OffStudy model (see also AdditionalEntryBucket) 
    
    Use this along with BaseRegisteredSubjectModelAdmin()
    
    """

    registered_subject = models.OneToOneField(RegisteredSubject)            
    
    
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


def delete_unused_appointments(sender, **kwargs):
    
    """ delete unused appointments created upon INSERT of sender model 
    
    for example, in the model file...

        from bhp_registration.models import BaseRegisteredSubjectModel, delete_unused_appointments

        < your model class ... >

        @receiver(post_delete, sender=InfantEligibility)
        def my_delete_handler(sender, **kwargs):
            delete_unused_appointments(sender, visit_model_name='infantvisit', **kwargs)    

    """
    
    instance = kwargs.get('instance')
    visit_model_name = kwargs.get('visit_model_name')
    Appointment.objects.delete_appointments_for_model(
                            registered_subject = instance.registered_subject, 
                            model_name = instance._meta.module_name,
                            visit_model_app_label = instance._meta.app_label,
                            visit_model_name = visit_model_name,
                            )    


