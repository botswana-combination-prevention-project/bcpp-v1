import re
from uuid import uuid4
from django.db import models
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


class BaseSubject (BaseSyncUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=36,
        blank=True,
        db_index=True,
        unique=True,
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

    def get_subject_identifier(self):
        return self.subject_identifier

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
        return (self.subject_identifier, )

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
        if not self.id and not self.subject_identifier:
            self.subject_identifier = str(uuid4())
        # never allow subject_identifier as None
        if not self.subject_identifier:
            raise ConsentError('Subject Identifier may not be left blank.')

    class Meta:
        abstract = True
