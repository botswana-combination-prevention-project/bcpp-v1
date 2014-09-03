from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from edc.base.model.validators import datetime_not_future, datetime_not_before_study_start, datetime_is_after_consent
from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.choices.common import GENDER_UNDETERMINED
from edc.choices.common import YES_NO
from edc.core.crypto_fields.fields import EncryptedFirstnameField, EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedLastnameField
from edc.device.sync.models import BaseSyncUuidModel

from ..managers import CorrectConsentManager

from .subject_consent import SubjectConsent


class CorrectConsent(BaseSyncUuidModel):

    """A model linked to the subject consent to record corrections."""

    subject_consent = models.OneToOneField(SubjectConsent)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )

    old_first_name = EncryptedFirstnameField()

    new_first_name = EncryptedFirstnameField(
        null=True,
        blank=True,
        )

    old_last_name = EncryptedLastnameField()

    new_last_name = EncryptedLastnameField(
        null=True,
        blank=True,
        )

    old_initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        )

    new_initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message='Ensure initials consist of letters only in upper case, no spaces.'), ],
        null=True,
        blank=True,
        )

    old_dob = models.DateField(
        verbose_name=_("Old Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        help_text=_("Format is YYYY-MM-DD"),
        )

    new_dob = models.DateField(
        verbose_name=_("New Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        null=True,
        blank=True,
        help_text=_("Format is YYYY-MM-DD"),
        )

    old_gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        max_length=1)

    new_gender = models.CharField(
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=True,
        )

    old_guardian_name = EncryptedLastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is '
                           '\'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        )

    new_guardian_name = EncryptedLastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                           'All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        )

    old_may_store_samples = models.CharField(
        verbose_name=_("Old Sample storage"),
        max_length=3,
        choices=YES_NO,
        )

    new_may_store_samples = models.CharField(
        verbose_name=_("New Sample storage"),
        max_length=3,
        blank=True,
        choices=YES_NO,
        )

    old_is_literate = models.CharField(
        verbose_name="(Old) Is the participant LITERATE?",
        max_length=3,
        choices=YES_NO,
        )

    new_is_literate = models.CharField(
        verbose_name="(New) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        choices=YES_NO,
        default='-',
        )

    history = AuditTrail()

    objects = CorrectConsentManager()

    def __unicode__(self):
        return unicode(self.subject_consent)

    def save(self, *args, **kwargs):
        self.compare_old_fields_to_consent()
        super(CorrectConsent, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_consent.natural_key()

    def compare_old_fields_to_consent(self, instance=None, exception_cls=None):
        """Raises an exception if an 'old_" field does not match the value
        on the corresponding subject_consent field."""
        exception_cls = exception_cls or ValidationError
        instance = instance or self
        # for each field prefixed with old compare to the consent
        for field in instance._meta.fields:
            if field.name.startswith('old_'):
                if not getattr(instance, field.name) == getattr(instance.subject_consent, field.name.split('old_')[1]):
                    print field.name
                    raise ValidationError("Consent \'{}\' does not match \'{}\'. Expected \'{}\'. Got \'{}\'.".format(
                        field.name.split('old_')[1],
                        field.name,
                        getattr(instance.subject_consent, field.name.split('old_')[1]),
                        getattr(instance, field.name) or None))

    def dashboard(self):
        ret = None
        if self.appointment:
            url = reverse('subject_dashboard_url',
                          kwargs={'dashboard_type': self.subject_consent.registered_subject.subject_type.lower(),
                                  'dashboard_model': 'appointment',
                                  'dashboard_id': self.appointment.pk,
                                  'show': 'appointments'})
            ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_subject'
