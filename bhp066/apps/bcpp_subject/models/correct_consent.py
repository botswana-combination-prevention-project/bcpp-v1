from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from edc.base.model.validators import (datetime_not_future, datetime_not_before_study_start,
                                       datetime_is_after_consent)
from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.choices.common import GENDER_UNDETERMINED
from edc.choices.common import YES_NO, YES
from edc.core.crypto_fields.fields import EncryptedFirstnameField, EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedLastnameField
from edc.device.sync.models import BaseSyncUuidModel

from ..managers import CorrectConsentManager

from .subject_consent import SubjectConsent
from .hic_enrollment import HicEnrollment


class CorrectConsent(BaseSyncUuidModel):

    """A model linked to the subject consent to record corrections."""

    subject_consent = models.OneToOneField(SubjectConsent)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )

    old_first_name = EncryptedFirstnameField(
            null=True,
            blank=True,
            )

    new_first_name = EncryptedFirstnameField(
        null=True,
        blank=True,
        )

    old_last_name = EncryptedLastnameField(
            null=True,
            blank=True,
            )
    new_last_name = EncryptedLastnameField(
        null=True,
        blank=True,
        )

    old_initials = EncryptedCharField(
        blank=True,
        null=True,
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
        null=True,
        blank=True,
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
        blank=True,
        null=True,
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
        blank=True,
        null=True,
        choices=YES_NO,
        )

    new_may_store_samples = models.CharField(
        verbose_name=_("New Sample storage"),
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
        )

    old_is_literate = models.CharField(
        verbose_name="(Old) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
        )

    new_is_literate = models.CharField(
        verbose_name="(New) Is the participant LITERATE?",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
        )

    old_witness_name = EncryptedLastnameField(
        verbose_name=_("Witness\'s Last and first name (illiterates only)"),
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        help_text=_('Required only if subject is illiterate. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
        )

    new_witness_name = EncryptedLastnameField(
        verbose_name=_("Witness\'s Last and first name (illiterates only)"),
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,
        help_text=_('Required only if subject is illiterate. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
        )

    history = AuditTrail()

    objects = CorrectConsentManager()

    def __unicode__(self):
        return unicode(self.subject_consent)

    def save(self, *args, **kwargs):
        self.compare_old_fields_to_consent()
        self.update_household_member_and_enrollment_checklist()
        super(CorrectConsent, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_consent.natural_key()

    def update_household_member_and_enrollment_checklist(self):
        #household member updates
        household_member = self.subject_consent.household_member
        enrollment_checklist = household_member.enrollment_checklist
        hic_enrollment = None
        if self.new_first_name:
            household_member.first_name = self.new_first_name
            self.subject_consent.first_name = self.new_first_name
            if self.new_last_name:
                household_member.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
                enrollment_checklist.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
                self.subject_consent.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
            else:
                household_member.initials = str(self.new_first_name)[0] + str(self.subject_consent.last_name)[0]
                enrollment_checklist.initials = str(self.new_first_name)[0] + str(self.subject_consent.last_name)[0]
                self.subject_consent.initials = str(self.new_first_name)[0] + str(self.subject_consent.last_name)[0]
        if self.new_initials:
            household_member.initials = self.new_initials
            enrollment_checklist.initials = self.new_initials
            self.subject_consent.initials = self.new_initials
        if self.new_gender:
            household_member.gender = self.new_gender
            enrollment_checklist.gender = self.new_gender
            self.subject_consent.gender = self.new_gender
        if self.new_dob:
            household_member.age_in_years = relativedelta(date.today(), self.new_dob).years
            enrollment_checklist.dob = self.new_dob
            self.subject_consent.dob = self.new_dob
            if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
                hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
                hic_enrollment.dob = self.new_dob
        if self.new_guardian_name:
            enrollment_checklist.guardian = YES
            self.subject_consent.guardian_name = self.new_guardian_name
        if self.new_is_literate:
            enrollment_checklist.literacy = self.new_is_literate
            self.subject_consent.is_literate = self.new_is_literate
            if self.new_is_literate == 'Yes':
                self.subject_consent.witness_name = None
            if self.new_witness_name:
                self.subject_consent.witness_name = self.new_witness_name
        if self.new_last_name:
            self.subject_consent.last_name = self.new_last_name
            if self.new_first_name:
                household_member.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
                enrollment_checklist.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
                self.subject_consent.initials = str(self.new_first_name)[0] + str(self.new_last_name)[0]
            else:
                household_member.initials = str(self.subject_consent.first_name)[0] + str(self.new_last_name)[0]
                enrollment_checklist.initials = str(self.subject_consent.first_name)[0] + str(self.new_last_name)[0]
                self.subject_consent.initials = str(self.subject_consent.first_name)[0] + str(self.new_last_name)[0]
        if self.new_witness_name:
            self.subject_consent.witness_name = self.new_witness_name
        if hic_enrollment:
            hic_enrollment.save(update_fields=['dob'])
        household_member.save(update_fields=['first_name', 'initials', 'gender', 'age_in_years'])
        enrollment_checklist.save(update_fields=['initials', 'gender', 'dob', 'literacy', 'guardian'])
        self.subject_consent.save(update_fields=['first_name', 'last_name', 'initials', 'gender', 'is_literate', 'witness_name', 'dob', 'guardian_name'])

    def compare_old_fields_to_consent(self, instance=None, exception_cls=None):
        """Raises an exception if an 'old_" field does not match the value
        on the corresponding subject_consent field."""
        exception_cls = exception_cls or ValidationError
        instance = instance or self
        # for each field prefixed with old compare to the consent
        for field in instance._meta.fields:
            if field.name.startswith('old_'):
                if getattr(instance, field.name):
                    if not getattr(instance, field.name) == getattr(instance.subject_consent, field.name.split('old_')[1]):
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
