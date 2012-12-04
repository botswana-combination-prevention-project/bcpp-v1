from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from audit_trail.audit import AuditTrail
from bhp_variables.models import StudySite
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_dispatch.models import DispatchItem
from bhp_appointment.managers import AppointmentManager
from bhp_appointment_helper.classes import AppointmentDateHelper
from base_appointment import BaseAppointment


class Appointment(BaseAppointment):

    """Tracks appointments for a registered subject's visit.

        Only one appointment per subject visit_definition+visit_instance.
        Attribute 'visit_instance' should be populated by the system
    """
    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')

    best_appt_datetime = models.DateTimeField(null=True, editable=False)

    study_site = models.ForeignKey(StudySite, null=True, blank=False)

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

    def natural_key(self):
        return (self.visit_instance, ) + self.visit_definition.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['bhp_registration.registeredsubject', 'bhp_visit.visitdefinition']

    def save(self, *args, **kwargs):
        appointment_date_helper = AppointmentDateHelper()
        if not self.id:
            self.appt_datetime = appointment_date_helper.get_best_datetime(self.appt_datetime, self.study_site)
            self.best_appt_datetime = self.appt_datetime
        else:
            if not self.best_appt_datetime:
                # did you update best_appt_datetime for existing instances since the migration?
                raise TypeError('Appointment instance attribute \'best_appt_datetime\' cannot be null on change.')
            self.appt_datetime = appointment_date_helper.change_datetime(self.best_appt_datetime, self.appt_datetime, self.study_site, self.visit_definition)
        super(Appointment, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s for %s.%s" % (self.registered_subject, self.visit_definition.code, self.visit_instance)

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('dashboard_url', kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                                       'subject_identifier': self.registered_subject.subject_identifier,
                                                       'appointment': self.pk})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

#    def natural_key_as_dict(self):
#        return {'registered_subject': self.registered_subject,
#                'visit_definition': self.visit_definition,
#                'visit_instance': self.visit_instance}

    def get_absolute_url(self):
        return reverse('admin:bhp_appointment_appointment_change', args=(self.id,))

    @property
    def is_dispatched(self):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        locked, producer = self.is_dispatched_to_producer()
        return locked

    def is_dispatched_to_producer(self):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        locked = False
        producer = None
        if DispatchItem.objects.filter(
                subject_identifiers__icontains=self.registered_subject.subject_identifier,
                is_dispatched=True).exists():
            dispatch_item = DispatchItem.objects.get(
                subject_identifiers__icontains=self.registered_subject.subject_identifier,
                is_dispatched=True)
            producer = dispatch_item.producer
            locked = True
        return locked, producer

    class Meta:
        ordering = ['registered_subject', 'appt_datetime', ]
        app_label = 'bhp_appointment'
