from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import NameField, DobField, InitialsField
from bhp_common.validators import datetime_is_future, date_not_future
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_visit.choices import APPT_STATUS

"""
    An appointment covers ONE VisitTracking record. 
    So the user must make an appointment before tracking the visit.
    
    Subject must be consented before making an appointment
    
"""    

class BaseAppointmentModel (MyBasicUuidModel):

    appt_datetime = models.DateTimeField(
        verbose_name=_("Appointment date and time"),
        help_text="",
        validators=[datetime_is_future,],
        )
    appt_status = models.CharField(
        verbose_name = _("Status"),
        choices=APPT_STATUS,
        max_length=25,
        )
    contact_tel = models.CharField(
        verbose_name = _("Contact Tel"), 
        max_length=250, 
        blank=True,
        )
    comment = models.CharField("Comment", 
        max_length=250, 
        blank=True,
        )        
        
    class Meta:
        abstract=True        


class GeneralAppointment(BaseAppointmentModel): 

    first_name = NameField(
        verbose_name = _("First name"),
        max_length=25,
        )

    initials = InitialsField()
    
    dob = DobField(
        validators=[date_not_future,],
        )

    visit_reason = models.CharField(
        verbose_name=_("Reason for visit"), 
        max_length = 25,
        help_text=_("Reason for visit"),
        )


class RegisteredSubjectAppointment(BaseAppointmentModel):

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
        help_text=_("A decimal to represent an additional report to be included with the original visit report. (NNNN.0)"),    
        )     

    def __unicode__(self):
        return "%s for %s [%s - %s]" % (self.registered_subject, self.visit_definition.code, self.appt_datetime, self.appt_status) 

    class Meta:
        unique_together = [('registered_subject', 'visit_definition', 'visit_instance')]


