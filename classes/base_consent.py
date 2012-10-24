from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_crypto.fields import EncryptedLastnameField, EncryptedTextField
from bhp_crypto.utils import mask_encrypted
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite
from bhp_subject.classes import BaseSubject
from consented_subject_identifier import ConsentedSubjectIdentifier
from bhp_appointment_helper.classes import AppointmentHelper


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

    comment = EncryptedTextField("Comment",
        max_length=250,
        blank=True,
        null=True
        )

    is_verified = models.BooleanField(default=False, editable=False)

    is_verified_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.subject_identifier, mask_encrypted(self.first_name), self.initials)

    def save_new_consent(self):
        """ Creates or gets a subject identifier and updates registered subject.

        Users may override this to change the default behavior for new instances"""
        consented_subject_identifier = ConsentedSubjectIdentifier()
        try:
            registered_subject = getattr(self, 'registered_subject')
        except:
            registered_subject = None
        # check for  registered subject key and if it already has
        # a subject_identifier (e.g for subjects re-consenting)
        if registered_subject:
            self.subject_identifier = self.registered_subject.subject_identifier
        if not self.subject_identifier:
            self.subject_identifier = consented_subject_identifier.get_identifier(
                consent=self,
                consent_attrname='subject_identifier',
                registration_status='consented',
                site_code=self.study_site.site_code)

    def save(self, *args, **kwargs):
        if not self.id:
            self.save_new_consent()
        super(BaseConsent, self).save(*args, **kwargs)
        # if has key to registered subject, might be a membership form
        # so need to create appointments
        if 'registered_subject' in dir(self):
            if not kwargs.get('suppress_autocreate_on_deserialize', False):
                AppointmentHelper().create_all(self.registered_subject, self.__class__.__name__.lower())

    class Meta:
        abstract = True
