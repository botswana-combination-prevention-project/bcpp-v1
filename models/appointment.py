from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import BaseAppointment
from bhp_visit.models import VisitDefinition

class Appointment(BaseAppointment):

    registered_subject = models.ForeignKey(RegisteredSubject) 
        
    """visit_definition is the visit code plus other information"""    
    visit_definition = models.ForeignKey(VisitDefinition,
        verbose_name=_("Visit"),
        help_text = _("For tracking within the window period of a visit, use the decimal convention. Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"),
        )
        
    """visit_instance should be populated by the system"""    
    visit_instance = models.IntegerField(
        verbose_name=_("Instance"),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9),
            ],
        default = 0,    
        null = True,
        blank = True,    
        help_text=_("A decimal to represent an additional report to be included with the original visit report. (NNNN.0)"),    
        )     

    def __unicode__(self):
        return "%s for %s.%s [%s - %s]" % (self.registered_subject, self.visit_definition.code, self.visit_instance,self.appt_datetime, self.appt_status) 

    def get_absolute_url(self):
        return reverse('admin:bhp_visit_appointment_change', args=(self.id,))

    class Meta:
        unique_together = [('registered_subject', 'visit_definition', 'visit_instance',),]
        ordering = ['registered_subject','appt_datetime', ]
        app_label = 'bhp_visit' 




