from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from audit_trail.audit import AuditTrail
from bhp_variables.models import StudySite
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.managers import AppointmentManager
from bhp_appointment.choices import APPT_TYPE
from base_appointment import BaseAppointment
from bhp_visit.classes import WindowPeriod
from bhp_appointment_helper.classes import AppointmentHelper


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
        verbose_name=("Visit"),
        help_text=("For tracking within the window period of a visit, use the decimal convention. "
                    "Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"))
    visit_instance = models.CharField(
        max_length=1,
        verbose_name=("Instance"),
        validators=[RegexValidator(r'[0-9]', 'Must be a number from 0-9')],
        default='0',
        null=True,
        blank=True,
        db_index=True,
        help_text=("A decimal to represent an additional report to be included with the original "
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
        help_text='Default for subject may be edited in admin under section bhp_subject. See Subject Configuration.')

    history = AuditTrail()

    objects = AppointmentManager()

    def natural_key(self):
        return (self.visit_instance, ) + self.visit_definition.natural_key() + self.registered_subject.natural_key()
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

    def validate_visit_instance(self, using=None, exception_cls=None):
        """Confirms a 0 instance appointment exists before allowing a continuation appt and keep a sequence."""
        if not exception_cls:
            exception_cls = ValidationError
        if not isinstance(self.visit_instance, basestring):
            raise exception_cls('Expected \'visit_instance\' to be of type basestring')
        if self.visit_instance != '0':
            if not Appointment.objects.using(using).filter(
                    registered_subject=self.registered_subject,
                    visit_definition=self.visit_definition,
                    visit_instance='0').exclude(pk=self.pk).exists():
                raise exception_cls('Cannot create continuation appointment for visit %s. Cannot find the original appointment (visit instance equal to 0).' % (self.visit_definition,))
            if int(self.visit_instance) - 1 != 0:
                if not Appointment.objects.using(using).filter(
                        registered_subject=self.registered_subject,
                        visit_definition=self.visit_definition,
                        visit_instance=str(int(self.visit_instance) - 1)).exists():
                    raise exception_cls('Cannot create continuation appointment for visit {0}. '
                                        'Expected next visit instance to be {1}. Got {2}'.format(self.visit_definition,
                                                                                                 str(int(self.visit_instance) - 1),
                                                                                                 self.visit_instance))

    def check_window_period(self, exception_cls=None):
        if not exception_cls:
            exception_cls = ValidationError
        if self.id:
            window_period = WindowPeriod()
            if not window_period.check_datetime(self.visit_definition, self.appt_datetime, self.best_appt_datetime):
                raise exception_cls(window_period.error_message)

    def save(self, *args, **kwargs):
        using = kwargs.get('using')
        self.appt_datetime, self.best_appt_datetime = self.validate_appt_datetime()
        self.check_window_period()
        self.validate_visit_instance(using=using)
        AppointmentHelper().check_appt_status(self, using)
        super(Appointment, self).save(*args, **kwargs)

    def raw_save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)

#     def check_appt_status(self, using):
#         """Checks the appt_status relative to the visit tracking form and ScheduledEntryBucket.
#         """
#         # for an existing appointment, check if there is a visit tracking form already on file
#         if not self.visit_definition.visit_tracking_content_type_map:
#             raise ImproperlyConfigured('Unable to determine the visit tracking model. Update bhp_visit.visit_definition {0} and select the correct visit model.'.format(self.visit_definition))
#         if not self.visit_definition.visit_tracking_content_type_map.model_class().objects.filter(appointment=self):
#             # no visit tracking, can only be New or Cqncelled
#             if self.appt_status not in ['new', 'cancelled']:
#                 self.appt_status = 'new'
#         else:
#             # have visit tracking, can only be Done, Incomplete, In Progress
#             visit_model_instance = self.visit_definition.visit_tracking_content_type_map.model_class().objects.get(appointment=self)
#             scheduled_entry = ScheduledEntry()
#             x = scheduled_entry.show_scheduled_entries(self.registered_subject, visit_model_instance=visit_model_instance)
#             if visit_model_instance.reason in visit_model_instance.get_visit_reason_no_follow_up_choices():
#                 # visit reason implies no data will be collected, so set appointment to Done
#                 self.appt_status = 'done'
#             else:
#                 ScheduledEntryBucket = get_model('bhp_entry', 'ScheduledEntryBucket')
#                 # set to in progress, if not already set
#                 if self.appt_status in ['done', 'incomplete']:
#                     # test if Done or Incomplete
#                     if ScheduledEntryBucket.objects.filter(appointment=self, entry_status='NEW').exists():
#                         #objs = ScheduledEntryBucket.objects.filter(appointment=self, entry_status='NEW')
#                         self.appt_status = 'incomplete'
#                     else:
#                         self.appt_status = 'done'
#                 elif self.appt_status in ['new', 'cancelled', 'in_progress']:
#                     self.appt_status = 'in_progress'
#                     # only one appointment can be "in_progress", so look for any others in progress and change
#                     # to Done or Incomplete, depending on ScheduledEntryBucket (if any NEW => incomplete)
#                     ScheduledEntryBucket = get_model('bhp_entry', 'ScheduledEntryBucket')
#                     for appointment in self.__class__.objects.filter(registered_subject=self.registered_subject, appt_status='in_progress').exclude(pk=self.pk):
#                         if ScheduledEntryBucket.objects.filter(appointment=appointment, entry_status='NEW').exists():
#                             # there are NEW forms
#                             if appointment.appt_status != 'incomplete':
#                                 appointment.appt_status = 'incomplete'
#                                 # call raw_save to avoid coming back to this method.
#                                 appointment.raw_save(using)
#                         else:
#                             # all forms are KEYED or NOT REQUIRED
#                             if appointment.appt_status != 'done':
#                                 appointment.appt_status = 'done'
#                                 # call raw_save to avoid coming back to this method.
#                                 appointment.raw_save(using)
#                 else:
#                     raise AppointmentStatusError('Did not expect appt_status == \'{0}\''.format(self.appt_status))

    def __unicode__(self):
        return "{0} {1} for {2}.{3}".format(self.registered_subject.subject_identifier, self.registered_subject.subject_type, self.visit_definition.code, self.visit_instance)

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('subject_dashboard_url',
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                      'dashboard_model': 'appointment',
                                      'dashboard_id': self.pk,
                                      'show': 'appointments'})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_registered_subject(self):
        return self.registered_subject

    def get_report_datetime(self):
        return self.appt_datetime

    class Meta:
        ordering = ['registered_subject', 'appt_datetime', ]
        app_label = 'bhp_appointment'
        unique_together = (('registered_subject', 'visit_definition', 'visit_instance'),)


#@receiver(post_save, weak=False, dispatch_uid="check_appt_status_on_post_save")
#def check_appt_status_on_post_save(sender, instance, raw, created, using, **kwargs):
#    if isinstance(instance, Appointment):
#        instance.post_save_check_appt_status(created, using)