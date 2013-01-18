from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_sync.models import BaseSyncUuidModel
from bhp_base_model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from bhp_common.choices import GENDER_UNDETERMINED
from bhp_base_model.fields import IsDateEstimatedField
from bhp_crypto.fields import EncryptedFirstnameField, EncryptedLastnameField


class BaseSubject (BaseSyncUuidModel):

    # may be null so uniqueness is enforce in save() if not null
    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=36,
        null=True,
        blank=True,
        db_index=True,
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

    def save(self, *args, **kwargs):
        # for new instances, enforce unique subject_identifier if not null
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.filter(subject_identifier=self.subject_identifier):
                raise ValidationError('Attempt to insert duplicate value for'
                                      'subject_identifier {0} when saving {1}.'.format(self.subject_identifier, self))
        super(BaseSubject, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s" % (self.subject_identifier, self.subject_type)

    class Meta:
        abstract = True
