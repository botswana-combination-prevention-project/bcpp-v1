from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.core.exceptions import ImproperlyConfigured
from bhp_sync.models import BaseSyncUuidModel
from bhp_common.choices import YES_NO
from bhp_crypto.fields import EncryptedLastnameField, EncryptedTextField
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start
from bhp_variables.models import StudySite
from bhp_consent.classes import ConsentHelper
from consent_catalogue import ConsentCatalogue
from bhp_consent.managers import BaseConsentUpdateManager
from base_consent import BaseConsent


class BaseConsentUpdate(BaseSyncUuidModel):
    """Tracks updates to the original consent.

    In the subclass:
        1. add your consent as a OneToOneField()::

            maternal_consent = models.OneToOneField(MaternalConsent)

        2. add a save method to update the main consent's most recent version number::

            def save(self, *args, **kwargs):
                #After save, updates the most recent consent version on the "entry" consent.
                super(MaternalConsentUpdate, self).save(*args, **kwargs)
                self.maternal_consent.consent_version_recent = self.consent_version
    """

    consent_catalogue = models.ForeignKey(ConsentCatalogue)

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
        verbose_name=_("Sample storage after closure?"),
        max_length=3,
        choices=YES_NO,
        help_text=_("Subject agrees for samples to be stored after the study closure")
        )

    comment = EncryptedTextField("Comment",
        max_length=250,
        blank=True,
        null=True
        )

    consent_version = models.IntegerField(null=True)

    objects = BaseConsentUpdateManager()

    def natural_key(self):
        return self.get_consent() + (self.consent_version, ) + self.get_consent_field().natural_key()

    def get_consent(self):
        for field in self._meta.fields:
            if field.rel:
                if 'to' in dir(field.rel):
                    if issubclass(field.rel.to, BaseConsent):
                        return (field.name, field.rel.to)
        raise ImproperlyConfigured('Method \'get_consent\' must be return a tuple of (attrname, model_cls) for the model attribute that is a subclass of BaseConsent. Does this model have a foreign key to a consent?')

    def get_report_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        if not self.consent_catalogue:
            super(BaseConsentUpdate, self).save(*args, **kwargs)
        self.consent_version = ConsentHelper(self).get_current_consent_version(self.consent_catalogue.name, self.consent_datetime)
        super(BaseConsentUpdate, self).save(*args, **kwargs)

    class Meta:
        abstract = True
