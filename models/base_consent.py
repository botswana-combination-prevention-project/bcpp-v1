from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_crypto.fields import EncryptedLastnameField, EncryptedTextField
from bhp_crypto.utils import mask_encrypted
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start, eligible_if_no
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite
from bhp_subject.models import BaseSubject
from bhp_appointment_helper.classes import AppointmentHelper
from bhp_common.utils import formatted_age
from bhp_consent.exceptions import ConsentError
from bhp_consent.classes import ConsentedSubjectIdentifier


class BaseConsent(BaseSubject):

    """ Consent models should be subclasses of this """

    study_site = models.ForeignKey(StudySite,
        verbose_name='Site',
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
        )

    consent_datetime = models.DateTimeField("Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        )

    guardian_name = EncryptedLastnameField(
        verbose_name=_("Guardian\'s Last and first name (minors only)"),
        validators=[
            RegexValidator('^[A-Z]{1,50}\,[A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME,FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        help_text=_('Required only if subject is a minor. Format is \'LASTNAME,FIRSTNAME\'. All uppercase separated by a comma'),
        )

    may_store_samples = models.CharField(
        verbose_name=_("Sample storage"),
        max_length=3,
        choices=YES_NO,
        help_text=_("Does the subject agree to have samples stored after the study has ended")
        )

    is_incarcerated = models.CharField(
        verbose_name="Is the participant under involuntary incarceration?",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_no, ],
        default='No',
        help_text="( if 'YES' STOP patient cannot be consented )",
        )

    comment = EncryptedTextField("Comment",
        max_length=250,
        blank=True,
        null=True
        )

    consent_version_on_entry = models.IntegerField(
        editable=False,
        default=1,
        help_text='Version of subject\'s initial consent.'
        )

    consent_version_recent = models.IntegerField(
        editable=False,
        default=1,
        help_text='Version of subject\'s most recent consent.'
        )

    is_verified = models.BooleanField(default=False, editable=False)

    is_verified_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.subject_identifier, mask_encrypted(self.first_name), self.initials)

    def _get_user_provided_subject_identifier(self):
        """Return a user provided subject_identifier.

        Do not override."""
        if self.get_user_provided_subject_identifier_attrname() in dir(self):
            return getattr(self, self.get_user_provided_subject_identifier_attrname())
        else:
            return None

    def get_user_provided_subject_identifier_attrname(self):
        """Override to return the attribute name of the user provided subject_identifier."""
        return None

    def save_new_consent(self, subject_identifier=None):
        """ Users may override this to compliment the default behavior for new instances.
        
        Must return a subject_identifier or None."""
        return subject_identifier

    def _save_new_consent(self):
        """ Creates or gets a subject identifier and updates registered subject.
        
        Also, calls user method :func:`save_new_consent`"""
        consented_subject_identifier = ConsentedSubjectIdentifier()
        try:
            registered_subject = getattr(self, 'registered_subject')
        except:
            registered_subject = None

        subject_identifier = self.save_new_consent(self.subject_identifier)

        if not subject_identifier:
            # test for user provided subject_identifier field method
            if self.get_user_provided_subject_identifier_attrname():
                self.subject_identifier = self._get_user_provided_subject_identifier()
                if self.subject_identifier and not registered_subject:
                    RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
                    RegisteredSubject.objects.update_with(self, 'subject_identifier', registration_status='consented', site_code=self.study_site.site_code)
            # try to get from registered_subject
            if not self.subject_identifier:
                if registered_subject:
                    if registered_subject.subject_identifier:
                        # check for  registered subject key and if it already has
                        # a subject_identifier (e.g for subjects re-consenting)
                        self.subject_identifier = self.registered_subject.subject_identifier
            # create a subject identifier, if not already done
            if not self.subject_identifier:
                self.subject_identifier = consented_subject_identifier.get_identifier(
                    consent=self,
                    consent_attrname='subject_identifier',
                    registration_status='consented',
                    site_code=self.study_site.site_code)

    def save(self, *args, **kwargs):
        # if editing, confirm that identifier fields are not changed
        if self.id:
            if self.get_user_provided_subject_identifier_attrname():
                if not self.subject_identifier == getattr(self, self.get_user_provided_subject_identifier_attrname()):
                    raise ConsentError('Identifier field {0} cannot be changed.'.format(self.get_user_provided_subject_identifier_attrname()))
        # if adding, call _save_new_consent()
        if not self.id:
            self._save_new_consent()
        # no matter what, make sure there is a subject_identifier
        if not self.subject_identifier:
            raise ConsentError("Subject identifier cannot be blank! It appears it was not provided or not generated")
        super(BaseConsent, self).save(*args, **kwargs)
        # if has key to registered subject, might be a membership form
        # so need to create appointments
        # TODO: is this required?? isn't this on a signal?
        if 'registered_subject' in dir(self):
            AppointmentHelper().create_all(self.registered_subject, self.__class__.__name__.lower())

    def formatted_age_at_consent(self):
        return formatted_age(self.dob, self.consent_datetime)

    @classmethod
    def get_consent_update_model(self):
        raise TypeError('The ConsentUpdateModel is required. Specify a class method get_consent_update_model() on the model to return the ConsentUpdateModel class.')

    def get_report_datetime(self):
        return self.consent_datetime

    class Meta:
        abstract = True
