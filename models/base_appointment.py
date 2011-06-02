from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import NameField, DobField, InitialsField
from bhp_common.validators import datetime_is_future, date_not_future
from bhp_registration.models import RegisteredSubject
from bhp_appointment.choices import APPT_STATUS

   

class BaseAppointment (MyBasicUuidModel):
    
    """Base model of appointments. """     
    
    appt_datetime = models.DateTimeField(
        verbose_name=_("Appointment date and time"),
        help_text="",
        #validators=[datetime_is_future,], check this at the form level...
        )
    appt_status = models.CharField(
        verbose_name = _("Status"),
        choices=APPT_STATUS,
        max_length=25,
        default='NEW',
        )
    appt_reason = models.CharField(
        verbose_name=_("Reason for appointment"), 
        max_length = 25,
        help_text=_("Reason for appointment"),
        blank=True,
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
