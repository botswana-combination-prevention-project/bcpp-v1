from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from choices import APPT_STATUS

"""
    An appointment covers ONE VisitTracking record. 
    So the user must make an appointment before tracking the visit.
    
    Subject must be consented before making an appointment
    
"""    
class Appointment (MyBasicUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject) 

    appt_datetime = models.DateTimeField(
        verbose_name="Appointment date and time",
        help_text="",
        validators=[datetime_is_future,],
        )
           
    appt_status = models.CharField(
        verbose_name = "Status",
        choices=APPT_STATUS,
        max_length=25,
        )
        
    """visit_definition is the visit code plus other information"""    
    visit_definition = models.ForeignKey(VisitDefinition,
        verbose_name="Visit",
        help_text = "For tracking within the window period of a visit, use the decimal convention. Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)",
        )
        
    """visit_instance should be populated by the system"""    
    visit_instance = models.IntegerField(
        verbose_name="Instance",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9),
            ],
        help_text="A decimal to represent an additional report to be included with the original visit report. (NNNN.0)",    
        )     
    

    def __unicode__(self):
        return "%s for %s [%s - %s]" % (self.registered_subject, self.visit_definition.code, self.appt_datetime, self.appt_status) 

    class Meta:
        unique_together = [('registered_subject', 'visit_definition', 'visit_instance')]

      
