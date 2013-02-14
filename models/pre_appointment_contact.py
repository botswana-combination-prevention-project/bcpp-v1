from django.db import models
#from django.core.urlresolvers import reverse
from bhp_common.choices import YES_NO
from bhp_contact.models import BaseContactLogItem
from bhp_appointment.models import Appointment


class PreAppointmentContact(BaseContactLogItem):

    appointment = models.ForeignKey(Appointment)

    contact = models.CharField(
        verbose_name='Contacted?',
        max_length=10,
        choices=(('subject', 'Subject'), ('other', 'Other person'))
        )

    is_confirmed = models.CharField(
        verbose_name='Has subject confirmed',
        max_length=10,
        choices=YES_NO,
        )

    new_appt_datetime = models.DateTimeField(
        verbose_name='New appointment',
        null=True,
        blank=True,
        help_text='Complete only if subject wishes to change appointment date')

    class Meta:
        app_label = 'bhp_appointment'
