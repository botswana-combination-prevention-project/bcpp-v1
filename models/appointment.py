from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from audit_trail.audit import AuditTrail
from bhp_variables.models import StudySite
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.managers import AppointmentManager
from bhp_appointment.choices import APPT_TYPE
from base_appointment import BaseAppointment


class Appointment(BaseAppointment):

    """Tracks appointments for a registered subject's visit.

        Only one appointment per subject visit_definition+visit_instance.
        Attribute 'visit_instance' should be populated by the system.
    """
    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')

    best_appt_datetime = models.DateTimeField(null=True, editable=False)

    appt_close_datetime = models.DateTimeField(null=True, editable=False)

    study_site = models.ForeignKey(StudySite,
        null=True,
        blank=False)

    visit_definition = models.ForeignKey(VisitDefinition, related_name='+',
        verbose_name=_("Visit"),
        help_text=_("For tracking within the window period of a visit, use the decimal convention. "
                    "Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"))
    visit_instance = models.CharField(
        max_length=1,
        verbose_name=_("Instance"),
        validators=[RegexValidator(r'[0-9]', 'Must be a number from 0-9')],
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
        help_text='hold dashboard_type variable, set by dashboard')

    appt_type = models.CharField(
        verbose_name='Appointment type',
        choices=APPT_TYPE,
        default='clinic',
        max_length=20,
        help_text='Default is set in configuration.')

    objects = AppointmentManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.visit_instance, self.appt_status,) + self.visit_definition.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['bhp_registration.registeredsubject', 'bhp_visit.visitdefinition']

    def validate_appt_datetime(self, exception_cls=None):
        """Returns the appt_datetime, possibly adjusted, and the best_appt_datetime, the calculated ideal timepoint datetime.

        .. note:: best_appt_datetime is not editable by the user. If 'None', will raise an exception."""
        from bhp_appointment_helper.classes import AppointmentDateHelper
        # for tests
        if not exception_cls:
            exception_cls = ValidationError
        appointment_date_helper = AppointmentDateHelper()
        if not self.id:
            appt_datetime = appointment_date_helper.get_best_datetime(self.appt_datetime, self.study_site)
            best_appt_datetime = self.appt_datetime
        else:
            if not self.best_appt_datetime:
                # did you update best_appt_datetime for existing instances since the migration?
                raise exception_cls('Appointment instance attribute \'best_appt_datetime\' cannot be null on change.')
            #if not self.is_new_appointment():
            #    raise exception_cls('Appointment date can no longer be changed. Appointment is not \'New\'')
            appt_datetime = appointment_date_helper.change_datetime(self.best_appt_datetime, self.appt_datetime, self.study_site, self.visit_definition)
            best_appt_datetime = self.best_appt_datetime
        return appt_datetime, best_appt_datetime

    def validate_visit_instance(self, exception_cls=None):
        """Confirms a 0 instance appointment exists before allowing a continuation appt and keep a sequence."""
        if not exception_cls:
            exception_cls = ValidationError
        if not isinstance(self.visit_instance, basestring):
            raise exception_cls('Expected \'visit_instance\' to be of type basestring')
        if self.visit_instance != '0':
            if not Appointment.objects.filter(
                    registered_subject=self.registered_subject,
                    visit_definition=self.visit_definition,
                    visit_instance='0').exclude(pk=self.pk).exists():
                raise exception_cls('Cannot create continuation appointment for visit %s. Cannot find the original appointment (visit instance equal to 0).' % (self.visit_definition,))
            if int(self.visit_instance) - 1 != 0:
                if not Appointment.objects.filter(
                        registered_subject=self.registered_subject,
                        visit_definition=self.visit_definition,
                        visit_instance=str(int(self.visit_instance) - 1)).exists():
                    raise exception_cls('Cannot create continuation appointment for visit {0}. '
                                        'Expected next visit instance to be {1}. Got {2}'.format(self.visit_definition,
                                                                                                 str(int(self.visit_instance) - 1),
                                                                                                 self.visit_instance))

    def save(self, *args, **kwargs):
        self.appt_datetime, self.best_appt_datetime = self.validate_appt_datetime()
        self.validate_visit_instance()
        super(Appointment, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} for {1}.{2}".format (self.registered_subject, self.visit_definition.code, self.visit_instance)

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('dashboard_url', 
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
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

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.appt_datetime

    class Meta:
        ordering = ['registered_subject', 'appt_datetime', ]
        app_label = 'bhp_appointment'
        unique_together = (('registered_subject', 'visit_definition', 'visit_instance'),)
