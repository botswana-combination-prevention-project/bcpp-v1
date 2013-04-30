import re
from uuid import uuid4
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
try:
    from bhp_dispatch.models import BaseDispatchSyncUuidModel as BaseSyncUuidModel
except ImportError:
    from bhp_sync.models import BaseSyncUuidModel
from bhp_base_model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from bhp_common.choices import GENDER_UNDETERMINED
from bhp_base_model.fields import IsDateEstimatedField
from bhp_crypto.fields import EncryptedFirstnameField, EncryptedLastnameField
from bhp_consent.exceptions import ConsentError
from bhp_identifier.exceptions import IdentifierError
from bhp_subject.managers import BaseSubjectManager


class BaseSubject (BaseSyncUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        blank=True,
        db_index=True,
        unique=True,
        )

    # a signal changes subject identifier which messes up bhp_sync
    # this field is always available and is unique
    subject_identifier_as_pk = models.CharField(
        verbose_name="Subject Identifier as pk",
        max_length=50,
        null=True,
        db_index=True,
        #unique=True,
        )

    # may not be available when instance created (e.g. infants prior to birth report)
    first_name = EncryptedFirstnameField(
        null=True,
        )

    # may not be available when instance created (e.g. infants or household subject before consent)
    last_name = EncryptedLastnameField(
        verbose_name="Last name",
        null=True,
        )

    # may not be available when instance created (e.g. infants)
    initials = models.CharField(
        max_length=3,
        validators=[RegexValidator(regex=r'^[A-Z]{2,3}$',
                                    message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        )

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        null=True,
        blank=False,
        help_text=_("Format is YYYY-MM-DD"),
        )

    is_dob_estimated = IsDateEstimatedField(
        verbose_name=_("Is date of birth estimated?"),
        null=True,
        blank=False,
        )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=False,
        )

    subject_type = models.CharField(
        max_length=25,
        default='undetermined',
        null=True,
        )

    objects = BaseSubjectManager()

    def get_subject_identifier(self):
        return self.subject_identifier

    def post_save_get_or_create_registered_subject(self, **kwargs):
        """Creates or \'gets and updates\' the registered subject instance for this subject.

        Called by a post save signal.

        ..note:: RegisteredSubject also inherits fom BaseSubject. This method does nothing if \'self\' is an
                 instance of RegisteredSubject.
        """
        using = kwargs.get('using', None)
        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        if not isinstance(self, RegisteredSubject):
            if 'registered_subject' in dir(self):
                self.registered_subject.subject_identifier = self.subject_identifier
#                self.registered_subject.subject_identifier_as_pk = self.subject_identifier_as_pk
                self.registered_subject.study_site = self.study_site
                self.registered_subject.dob = self.dob
                self.registered_subject.is_dob_estimated = self.is_dob_estimated
                self.registered_subject.gender = self.gender
                self.registered_subject.initials = self.initials
                self.registered_subject.identity = self.identity
                self.registered_subject.first_name = self.first_name
                self.registered_subject.last_name = self.last_name
                if self.last_name:
                    self.registered_subject.registration_status = 'consented'
                self.registered_subject.subject_type = self.subject_type
                self.registered_subject.save(using=using)
            else:
                defaults = {
                    'subject_identifier': self.subject_identifier,
#                    'subject_identifier_as_pk': self.subject_identifier_as_pk,
                    'study_site': self.study_site,
                    'dob': self.dob,
                    'is_dob_estimated': self.is_dob_estimated,
                    'gender': self.gender,
                    'initials': self.initials,
                    'identity': self.identity,
                    'identity_type': self.identity_type,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'subject_type': self.subject_type}
                if self.last_name:
                    defaults.update({'registration_status': 'consented'})
                registered_subject, created = RegisteredSubject.objects.using(using).get_or_create(subject_identifier=self.subject_identifier, identity=self.identity, defaults=defaults)
                if not created:
                    for k in registered_subject.__dict__.iterkeys():
                        if k in defaults:
                            setattr(registered_subject, k, defaults.get(k))
                    registered_subject.save(using=using)

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        self.insert_dummy_identifier()
        self._check_if_duplicate_subject_identifier(using)
        self.check_if_may_change_subject_identifier(using)
        # if editing, confirm that identifier fields are not changed
        if self.id:
            if self.get_user_provided_subject_identifier_attrname():
                if not self.subject_identifier == getattr(self, self.get_user_provided_subject_identifier_attrname()):
                    raise IdentifierError('Identifier field {0} cannot be changed.'.format(self.get_user_provided_subject_identifier_attrname()))
        if not self.id:
            if self.get_user_provided_subject_identifier_attrname():
                # if user_provided_subject_identifier is None, set it to the same value as subject_identifier
                if not getattr(self, self.get_user_provided_subject_identifier_attrname()):
                    setattr(self, self.get_user_provided_subject_identifier_attrname(), self.subject_identifier)
        super(BaseSubject, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} {1}".format(self.mask_unset_subject_identifier(), self.subject_type)

    def natural_key(self):
        return (self.subject_identifier_as_pk, )

    def mask_unset_subject_identifier(self):
        subject_identifier = self.subject_identifier
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(subject_identifier):
            subject_identifier = '<identifier not set>'
        return subject_identifier

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

    def include_for_dispatch(self):
        return True

    def check_if_may_change_subject_identifier(self, using):
        if self.id:
            if not self.__class__.objects.get(pk=self.id).subject_identifier == self.subject_identifier:
                raise IdentifierError('Subject Identifier cannot be changed. Got {0} != {1}'.format(self.__class__.objects.get(pk=self.id).subject_identifier, self.subject_identifier))

    def _check_if_duplicate_subject_identifier(self, using):
        """Checks if the subject identifier is in use, for new and existing instances."""
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.using(using).filter(subject_identifier=self.subject_identifier):
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} when saving {1}.'.format(self.subject_identifier, self))
        else:
            if self.__class__.objects.using(using).filter(subject_identifier=self.subject_identifier).exclude(pk=self.pk):
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} when saving {1}.'.format(self.subject_identifier, self))
        self.check_for_duplicate_subject_identifier()

    def check_for_duplicate_subject_identifier(self):
        """Users may override to add an additional strategy to detect duplicate identifiers."""
        pass

    def insert_dummy_identifier(self):
        """Inserts a random uuid as a dummy identifier."""
        # set to uuid if new and not specified
        if not self.id:
            subject_identifier_as_pk = str(uuid4())
            self.subject_identifier_as_pk = subject_identifier_as_pk  # this will never change
            if not self.subject_identifier:
                self.subject_identifier = subject_identifier_as_pk  # this will be changed when allocated a subject_identifier on consent
        # never allow subject_identifier as None
        if not self.subject_identifier:
            raise ConsentError('Subject Identifier may not be left blank.')

    class Meta:
        abstract = True
