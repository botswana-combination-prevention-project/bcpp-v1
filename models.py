from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import NameField, DobField, InitialsField
from bhp_common.validators import datetime_is_future, date_not_future

from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition

"""
    An appointment covers ONE VisitTracking record. 
    So the user must make an appointment before tracking the visit.
    
    Subject must be consented before making an appointment
    
"""    

class BaseAppointmentModel (MyBasicUuidModel):

    subject_identifier = models.CharField(
        verbose_name = _("Subject identifier"),
        max_length = 36,
        editable=False,
        null=True,
        help_text = _("Subject identifier"),
        )
            
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
    first_name = NameField(
        verbose_name = _("First name"),
        max_length=25,
        )

    initials = InitialsField()
    
    dob = DobField(
        validators=[date_not_future,],
        )

    appt_reason = models.CharField(
        verbose_name=_("Reason for appointment"), 
        max_length = 25,
        help_text=_("Reason for appointment"),
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





