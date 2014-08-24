

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from apps.bcpp_subject.models.subject_consent import SubjectConsent
from apps.bcpp_subject.exceptions import OldConsentValueError


from edc.choices.common import GENDER_UNDETERMINED
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.core.crypto_fields.fields import EncryptedFirstnameField, EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedLastnameField
from edc.choices.common import YES_NO
from edc.device.dispatch.models import BaseDispatchSyncUuidModel


class CorrectConsent(BaseDispatchSyncUuidModel):

    """ Consent models should be subclasses of this """

    subject_consent = models.ForeignKey(SubjectConsent)

    # may not be available when instance created (e.g. infants prior to birth report)
    first_name = EncryptedFirstnameField(
        null=True,
        )

    first_name_old = EncryptedFirstnameField(
        null=True,
        )

    # may not be available when instance created (e.g. infants or household subject before consent)
    last_name = EncryptedLastnameField(
        verbose_name="Last name",
        null=True,
        )

    last_name_old = EncryptedLastnameField(
        verbose_name="Last name",
        null=True,
        )

    # may not be available when instance created (e.g. infants)
    initials = EncryptedCharField(
        validators=[RegexValidator(regex=r'^[A-Z]{2,3}$',
                                    message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        )

    initials_old = EncryptedCharField(
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

    dob_old = models.DateField(
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

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=False,
        )

    gender_old = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=False,
        )

    guardian_name = EncryptedLastnameField(
        verbose_name=("Guardian\'s Last and first name (minors only)"),
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        help_text=('Required only if subject is a minor. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma then followe by a space.'),
        )

    guardian_name_old = EncryptedLastnameField(
        verbose_name=("Guardian\'s Last and first name (minors only)"),
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        help_text=('Required only if subject is a minor. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma then followe by a space.'),
        )

    may_store_samples = models.CharField(
        verbose_name=_("Sample storage"),
        max_length=3,
        choices=YES_NO,
        help_text=("Does the subject agree to have samples stored after the study has ended")
        )

    may_store_samples_old = models.CharField(
            verbose_name=_("Sample storage"),
            max_length=3,
            choices=YES_NO,
            help_text=("Does the subject agree to have samples stored after the study has ended")
            )

    is_literate = models.CharField(
        verbose_name="Is the participant LITERATE?",
        max_length=3,
        choices=YES_NO,
        default='-',
        help_text="( if 'No' provide witness\'s name here and with signature on the paper document.)",
        )

    is_literate_old = models.CharField(
        verbose_name="Is the participant LITERATE?",
        max_length=3,
        choices=YES_NO,
        default='-',
        help_text="( if 'No' provide witness\'s name here and with signature on the paper document.)",
        )

    def save(self, *args, **kwargs):
        self.matches_old_consent_values()
        super(CorrectConsent, self).save(*args, **kwargs)

    def matches_old_consent_values(self):
        if self.first_name and not (self.first_name_old == self.subject_consent.first_name):
            raise OldConsentValueError("The existing subject first name: {0} does not match the old subject first name: {1} you are entering.".format(self.subject_consent.first_name, self.first_name_old))
        if self.last_name and not (self.last_name_old == self.subject_consent.last_name):
            raise OldConsentValueError("The existing subject last name: {0} does not match the old subject last name: {1} you are entering.".format(self.last_name_old, self.subject_consent.last_name))
        if self.initials and not (self.initials_old == self.subject_consent.initials):
            raise OldConsentValueError("The existing subject initials: {0} does not match the old subject initials: {1} you are entering.".format(self.initials_old, self.subject_consent.initials))
        if self.dob and not (self.dob_old == self.subject_consent.dob):
            raise OldConsentValueError("The existing subject date of birth: {0} does not match the old subject date of birth: {0} you are entering.".format(self.dob_old, self.subject_consent.dob))
        if self.gender and not (self.gender_old == self.subject_consent.gender):
            raise OldConsentValueError("The existing subject gender: {0} does not match the old subject gender: {1} you are entering.".format(self.gender_old, self.subject_consent.gender))
        if self.may_store_samples and not (self.may_store_samples_old == self.subject_consent.may_store_samples):
            raise OldConsentValueError("The existing subject sample storage value: {0} does not match the old subject sample storage value: {1} you are entering.".format(self.may_store_samples_old, self.subject_consent.may_store_samples))
        if self.is_literate and not (self.is_literate == self.subject_consent.is_literate):
            raise OldConsentValueError("The existing subject literacy:  {0} does not match the old subject literacy: {1} you are entering.".format(self.is_literate, self.subject_consent.is_literate))

    class Meta:
        app_label = 'bcpp_subject'
