from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from audit_trail.audit import AuditTrail
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.managers import AppointmentManager
from bhp_appointment.classes import AppointmentDate
from base_appointment import BaseAppointment


class Appointment(BaseAppointment):

    """Tracks appointments for a registered subject's visit.

        Only one appointment per subject visit_definition+visit_instance.
        Attribute 'visit_instance' should be populated by the system
    """
    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')

    best_appt_datetime = models.DateTimeField(null=True)

    visit_definition = models.ForeignKey(VisitDefinition, related_name='+',
        verbose_name=_("Visit"),
        help_text=_("For tracking within the window period of a visit, use the decimal convention. "
                    "Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"))
    visit_instance = models.CharField(
        max_length=1,
        verbose_name=_("Instance"),
        validators=[
            RegexValidator(r'[0-9]', 'Must be a number from 0-9'),
            ],
        default='0',
        null=True,
        blank=True,
        db_index=True,
        help_text=_("A decimal to represent an additional report to be included with the original "
                    "visit report. (NNNN.0)"))
    dashboard_type = models.CharField(
        max_length=25,
        editable=False,
        null=True,
        blank=True,
        db_index=True,
        help_text='hold dashboard_type variable, set by dashbaord')

    objects = AppointmentManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        appointment_date = AppointmentDate()
        if not self.id:
            self.appt_datetime = appointment_date.get(self.appt_datetime)
            self.best_appt_datetime = self.appt_datetime
        else:
            self.appt_datetime = appointment_date.change(self.best_appt_datetime, self.appt_datetime)
        super(Appointment, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s for %s.%s" % (self.registered_subject, self.visit_definition.code, self.visit_instance)

    def dashboard(self):
        url = reverse('dashboard_url', kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                               'subject_identifier': self.registered_subject.subject_identifier,
                                               'appointment': self.pk})
        ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    def natural_key_as_dict(self):
        return {'registered_subject': self.registered_subject,
                'visit_definition': self.visit_definition,
                'visit_instance': self.visit_instance}

    def get_absolute_url(self):
        return reverse('admin:bhp_appointment_appointment_change', args=(self.id,))

    class Meta:
        ordering = ['registered_subject', 'appt_datetime', ]
        app_label = 'bhp_appointment'
