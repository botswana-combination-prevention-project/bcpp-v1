import copy
from datetime import datetime
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from bhp_consent.models import BaseConsentedUuidModel
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_after_consent
from bhp_base_model.fields import OtherCharField
from bhp_appointment.models import Appointment
from bhp_visit_tracking.managers import BaseVisitTrackingManager
from bhp_visit_tracking.choices import VISIT_REASON
from bhp_visit_tracking.settings import VISIT_REASON_REQUIRED_CHOICES, VISIT_REASON_NO_FOLLOW_UP_CHOICES, VISIT_REASON_FOLLOW_UP_CHOICES


class BaseVisitTracking (BaseConsentedUuidModel):

    """Base model for Appt/Visit Tracking (AF002).

    For entry, requires an appointment be created first, so there
    is no direct reference to 'registered subject' in this model except
    thru appointment.

    List of appointments in admin.py should be limited to scheduled
    appointments for the current registered subject.

    Other ideas: ADD should only allow 'scheduled', and CHANGE only allow 'seen'
    Admin should change the status after ADD.

    """
    appointment = models.OneToOneField(Appointment)

    report_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )

    reason = models.CharField(
        verbose_name="What is the reason for this visit?",
        max_length=25,
        # this is commented out and handled in the ModelForm class, see comment just below...
        #choices=,
        help_text="<Override the field class for this model field attribute in ModelForm>",
        )

    """
        as each study will have variations on the 'reason' choices, allow this
        tuple to be defined at the form level. In the ModelForm add something
        like this:

        reason = forms.ChoiceField(
            label = 'Reason for visit',
            choices = [ choice for choice in VISIT_REASON ],
            help_text = "If 'unscheduled', information is usually reported at the next scheduled visit, but exceptions may arise",
            widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
            )

        where the choices tuple is defined in the local app.
    """

    reason_missed = models.CharField(
        verbose_name="If 'missed' above, Reason scheduled visit was missed",
        max_length=35,
        blank=True,
        null=True,
        )

    """
        ...same as above...Something like this:

        info_source = forms.ChoiceField(
            label = 'Source of information',
            choices = [ choice for choice in VISIT_INFO_SOURCE ],
            widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
            )
    """

    info_source = models.CharField(
        verbose_name="What is the main source of this information?",
        max_length=25,
        # this is commented out and handled in the ModelForm class
        #choices=VISIT_INFO_SOURCE,
        help_text="",
        )

    info_source_other = OtherCharField()

    """
        this value should be suggested by the sytem but may be edited by the user.
        A further 'save' check should confirm that the date makes sense relative
        to the visit schedule
    """

    comments = models.TextField(
        verbose_name="Comment if any additional pertinent information about the participant",
        max_length=250,
        blank=True,
        null=True,
        )

    """
    #TODO: add next_scheduled_visit_datetime but put in checks for the window period etc.
    next_scheduled_visit_datetime = models.DateTimeField(
        verbose_name="Next scheduled visit date and time",
        validators=[
            datetime_is_after_consent,
            datetime_is_future,
            ],
        )
    """

    objects = BaseVisitTrackingManager()

    def get_visit_reason_no_follow_up_choices(self):
        """Returns the visit reasons that do not imply any data collection; that is, the subject is not available."""
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        return dct

    def get_visit_reason_follow_up_choices(self):
        """Returns visit reasons that imply data is being collected; that is, subject is present."""
        dct = {}
        for item in VISIT_REASON_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        return dct

    def get_visit_reason_choices(self):
        """Returns a tuple of the reasons choices for the reason field."""
        return VISIT_REASON

    def _check_visit_reason_keys(self):
        user_keys = [tpl[0] for tpl in self.get_visit_reason_choices()]
        default_keys = copy.deepcopy(VISIT_REASON_REQUIRED_CHOICES)
        if list(set(default_keys) - set(user_keys)):
            user_keys = [k for k in self.get_visit_reason_no_follow_up_choices().iterkeys()] + [k for k in self.get_visit_reason_follow_up_choices().iterkeys()]
            missing_keys = list(set(default_keys) - set(user_keys))
            if missing_keys:
                raise ImproperlyConfigured(
                    'User\'s visit reasons tuple must contain all keys for no follow-up {1} and all for follow-up {2}. Missing {3}. '
                    'Override methods \'get_visit_reason_no_follow_up_choices\' and \'get_visit_reason_follow_up_choices\' on the visit model '
                    'if you are not using the default keys of {4}. '
                    'Got {0}'.format(
                        user_keys,
                        VISIT_REASON_NO_FOLLOW_UP_CHOICES,
                        VISIT_REASON_FOLLOW_UP_CHOICES,
                        missing_keys,
                        VISIT_REASON_REQUIRED_CHOICES))

    def _get_visit_reason_choices(self):
        """Returns a dictionary representing the visit model reason choices tuple.

        Depending on how well the local VISIT_REASON choices tuple conforms to the default,
        methods :func:`get_visit_reason_no_follow_up_choices` and :func:`get_visit_reason_follow_up_choices`
        are used to manipulate it so that it works with ScheduledEntry like the default.

        This is called by the ScheduledEntry class when deciding to delete or create
        NEW forms for entry on the dashboard."""

        self._check_visit_reason_keys()
        visit_reason_tuple = self.get_visit_reason_choices()
        # convert to dictionary
        visit_reason_choices = {}
        for tpl in visit_reason_tuple:
            visit_reason_choices.update({tpl[0]: tpl[1]})
        if not isinstance(visit_reason_choices, dict):
            raise TypeError('Method get_visit_reason_choices must return a dictionary or tuple of tuples. Got {0}'.format(visit_reason_choices))
        visit_reason_required_choices = copy.deepcopy(VISIT_REASON_REQUIRED_CHOICES)
        if 'get_visit_reason_no_follow_up_choices' in dir(self):
            visit_reason_no_follow_up_choices = self.get_visit_reason_no_follow_up_choices()
            if not isinstance(visit_reason_no_follow_up_choices, dict):
                raise TypeError('Method get_visit_reason_no_follow_up_choices must return a dictionary. Got {0}'.format(visit_reason_no_follow_up_choices))
            # ensure required keys are in no follow up
            for key, value in visit_reason_no_follow_up_choices.iteritems():
                if value not in visit_reason_required_choices:
                    visit_reason_required_choices.remove(key)
                    visit_reason_required_choices.append(value)
        if 'get_visit_reason_follow_up_choices' in dir(self):
            visit_reason_follow_up_choices = self.get_visit_reason_follow_up_choices()
            if not isinstance(visit_reason_follow_up_choices, dict):
                raise TypeError('Method visit_reason_follow_up_choices must return a dictionary. Got {0}'.format(visit_reason_follow_up_choices))
            # ensure required keys are in follow up
            for key, value in visit_reason_follow_up_choices.iteritems():
                if value not in visit_reason_required_choices:
                    visit_reason_required_choices.remove(key)
                    visit_reason_required_choices.append(value)
        copy_visit_reason_choices = copy.deepcopy(visit_reason_choices)
        copy_visit_reason_choices = [x.lower() for x in copy_visit_reason_choices]
        for k in visit_reason_required_choices:
            if k.lower() not in copy_visit_reason_choices:
                raise ImproperlyConfigured('Dictionary returned by get_visit_reason_choices() must have keys {0}. Got {1} with {2}'.format(visit_reason_required_choices, visit_reason_choices.keys(), k))
        return visit_reason_choices

    def post_save_check_in_progress(self):
        #set other appointments that are in progress to incomplete
        dirty = False
        this_appt_tdelta = datetime.today() - self.appointment.appt_datetime
        if this_appt_tdelta.days == 0:
            # if today is the appointment, set to self.appointment in progress and
            # the others to incomplete if not 'done' and not 'cancelled'
            appointments = self.appointment.__class__.objects.filter(registered_subject=self.appointment.registered_subject,
                                                      appt_status='in_progress')
            for appointment in appointments:
                tdelta = datetime.today() - self.appointment.appt_datetime
                if tdelta.days < 0 and appointment.appt_status != 'done' and appointment.appt_status != 'cancelled':
                    appointment.appt_status = 'incomplete'
                    self.appointment.save()
            # set self.appointment to in_progress
            self.appointment.appt_status = 'in_progress'
            dirty = True
        elif this_appt_tdelta.days > 0 and self.appointment.appt_status != 'done' and self.appointment.appt_status != 'cancelled':
            # self.appointment is in the past
            self.appointment.appt_status = 'incomplete'
            dirty = True
        elif this_appt_tdelta.days < 0 and self.appointment.appt_status != 'cancelled':
            # self.appointment is in the future
            self.appointment.appt_status = 'new'
            dirty = True
        else:
            pass
        if dirty:
            self.appointment.save()

    def natural_key(self):
        return (self.report_datetime, ) + self.appointment.natural_key()
    natural_key.dependencies = ['bhp_appointment.appointment', ]

    def get_subject_identifier(self):
        return self.get_registered_subject().subject_identifier

    def get_report_datetime(self):
        return self.report_datetime

    def get_registered_subject(self):
        return self.appointment.registered_subject

    class Meta:
        abstract = True
