from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_registration.models import RegisteredSubject
from bhp_form.models import VisitDefinition, ScheduleGroup
from base_appointment import BaseAppointment

class AppointmentManager(models.Manager):
    
    def create_appointments(self, **kwargs):

        """Create appointments based on a list of visit definitions if given model_name is a member of a schedule group.
    
        Only create for visit_instance = 0
        If appointment exists, just update the appt_datetime
        """
        
        registered_subject = kwargs.get("registered_subject")
        model_name = kwargs.get("model_name")
        base_appt_datetime = kwargs.get("base_appt_datetime")
        
        if ScheduleGroup.objects.filter(membership_form__content_type_map__model = model_name):
            # get list of visits for scheduled group containing this model
            visits = VisitDefinition.objects.filter(schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model = model_name))
            for visit in visits:
                # if appt exists, update appt_datetime
                if super(AppointmentManager, self).filter(
                            registered_subject = registered_subject, 
                            visit_definition = visit, 
                            visit_instance = 0):
                    appt = Appointment.objects.get(
                                registered_subject = registered_subject, 
                                visit_definition = visit, 
                                visit_instance = 0)
                    appt.app_datetime = base_appt_datetime
                    appt.save()
                # else create a new appointment                    
                else:
                    super(AppointmentManager, self).create(
                        registered_subject = registered_subject,
                        visit_definition = visit,
                        visit_instance = 0,
                        appt_datetime = base_appt_datetime,
                        )


class Appointment(BaseAppointment):

    """Model to track appointments for a registered subject's visit.
        
    Only one appointment per subject visit_definition+visit_instance.
    Attribute 'visit_instance' should be populated by the system    
    """    
    
    registered_subject = models.ForeignKey(RegisteredSubject) 
        

    visit_definition = models.ForeignKey(VisitDefinition,
        verbose_name=_("Visit"),
        help_text = _("For tracking within the window period of a visit, use the decimal convention. Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"),
        )

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

    objects = AppointmentManager()

    def __unicode__(self):
        return "%s for %s.%s [%s - %s]" % (self.registered_subject, self.visit_definition.code, self.visit_instance,self.appt_datetime, self.appt_status) 

    def get_absolute_url(self):
        return reverse('admin:bhp_visit_appointment_change', args=(self.id,))

    class Meta:
        unique_together = [('registered_subject', 'visit_definition', 'visit_instance',),]
        ordering = ['registered_subject','appt_datetime', ]
        app_label = 'bhp_visit' 

