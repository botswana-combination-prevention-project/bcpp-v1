from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import FirstnameField, EncryptedCharField, LastnameField
from edc_base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc_consent.models.validators import AgeTodayValidator
from edc_constants.choices import GENDER_UNDETERMINED, YES_NO, YES

from ..managers import CorrectConsentManager

from .hic_enrollment import HicEnrollment
from .subject_consent import SubjectConsent


class BaseCorrectConsent(models.Model):

    """A model linked to the subject consent to record corrections."""

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
    )

    old_first_name = FirstnameField(
        null=True,
        blank=True,
    )

    new_first_name = FirstnameField(
        null=True,
        blank=True,
    )

    old_last_name = LastnameField(
        null=True,
        blank=True,
    )
    new_last_name = LastnameField(
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
        verbose_name="Old Date of birth",
        null=True,
        blank=True,
        validators=[AgeTodayValidator(16, 64)],
        help_text="Format is YYYY-MM-DD",
    )

    new_dob = models.DateField(
        verbose_name="New Date of birth",
        validators=[AgeTodayValidator(16, 64)],
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD",
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

    old_guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is '
                           '\'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    new_guardian_name = LastnameField(
        validators=[
            RegexValidator('^[A-Z]{1,50}\, [A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. '
                           'All uppercase separated by a comma')],
        blank=True,
        null=True,
    )

    old_may_store_samples = models.CharField(
        verbose_name="Old Sample storage",
        max_length=3,
        blank=True,
        null=True,
        choices=YES_NO,
    )

    new_may_store_samples = models.CharField(
        verbose_name="New Sample storage",
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

    old_witness_name = LastnameField(
        verbose_name="Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

    new_witness_name = LastnameField(
        verbose_name="Witness\'s Last and first name (illiterates only)",
        validators=[
            RegexValidator(
                '^[A-Z]{1,50}\, [A-Z]{1,50}$',
                'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma')],
        blank=True,
        null=True,
        help_text=('Required only if subject is illiterate. Format is \'LASTNAME, FIRSTNAME\'. '
                   'All uppercase separated by a comma'),
    )

    def save(self, *args, **kwargs):
        self.compare_old_fields_to_consent()
        self.update_household_member_and_enrollment_checklist()
        super(BaseCorrectConsent, self).save(*args, **kwargs)

    def compare_old_fields_to_consent(self, instance=None, exception_cls=None):
        """Raises an exception if an 'old_" field does not match the value
        on the corresponding subject_consent field."""
        exception_cls = exception_cls or ValidationError
        instance = instance or self
        for field in instance._meta.fields:
            if field.name.startswith('old_'):
                old_value = getattr(instance, field.name)
                new_value = getattr(instance, 'new_{}'.format(field.name.split('old_')[1]))
                if (not old_value and new_value) or (old_value and not new_value):
                    raise exception_cls(
                        'Both the old and new value must be provided. Got \'{}\' and \'{}\'. See {}'.format(
                            old_value, new_value, field.name))
                elif old_value and new_value and old_value == new_value:
                    raise exception_cls(
                        'The old and new value are equal. Got \'{}\' and \'{}\'. See {}'.format(
                            old_value, new_value, field.name))
                elif old_value and new_value:
                    subject_consent_value = getattr(instance.subject_consent, field.name.split('old_')[1])
                    if old_value != subject_consent_value:
                        raise exception_cls(
                            "Consent \'{}\' does not match \'{}\'. Expected \'{}\'. Got \'{}\'.".format(
                                field.name.split('old_')[1],
                                field.name,
                                subject_consent_value,
                                old_value))

    def update_household_member_and_enrollment_checklist(self):
        try:
            enrollment_checklist = self.enrollment_checklist
        except AttributeError:
            enrollment_checklist = self.subject_consent.household_member.enrollment_checklist
        self.update_name_and_initials(enrollment_checklist)
        self.update_gender(enrollment_checklist)
        self.update_dob(enrollment_checklist)
        self.update_guardian_name(enrollment_checklist)
        self.update_is_literate(enrollment_checklist)
        self.update_witness()
        self.subject_consent.household_member.save(
            update_fields=['first_name', 'initials', 'gender', 'age_in_years'])
        enrollment_checklist.save(
            update_fields=['initials', 'gender', 'dob', 'literacy', 'guardian'])
        self.subject_consent.save(update_fields=[
            'first_name', 'last_name', 'initials', 'gender',
            'is_literate', 'witness_name', 'dob', 'guardian_name'])

    def update_initials(self, first_name, last_name):
        initials = '{}{}'.format(first_name[0], last_name[0])
        if self.new_initials:
            if self.new_initials.startswith(initials[0]) and self.new_initials.endswith(initials[-1]):
                initials = self.new_initials
            else:
                raise ValidationError(
                    'New initials do not match first and last name. Expected {}, Got {}'.format(
                        initials, self.new_initials))
        return initials

    def update_gender(self, enrollment_checklist):
        if self.new_gender:
            self.subject_consent.household_member.gender = self.new_gender
            enrollment_checklist.gender = self.new_gender
            self.subject_consent.gender = self.new_gender

    def update_dob(self, enrollment_checklist):
        if self.new_dob:
            self.subject_consent.household_member.age_in_years = relativedelta(
                date.today(), self.new_dob).years
            enrollment_checklist.dob = self.new_dob
            self.subject_consent.dob = self.new_dob
            try:
                hic_enrollment = HicEnrollment.objects.get(
                    subject_visit__household_member=self.subject_consent.household_member)
                hic_enrollment.dob = self.new_dob
                hic_enrollment.save(update_fields=['dob'])
            except HicEnrollment.DoesNotExist:
                pass

    def update_guardian_name(self, enrollment_checklist):
        if self.new_guardian_name:
            enrollment_checklist.guardian = YES
            self.subject_consent.guardian_name = self.new_guardian_name

    def update_is_literate(self, enrollment_checklist):
        if self.new_is_literate:
            enrollment_checklist.literacy = self.new_is_literate
            self.subject_consent.is_literate = self.new_is_literate
            if self.new_is_literate == YES:
                self.subject_consent.witness_name = None
            if self.new_witness_name:
                self.subject_consent.witness_name = self.new_witness_name

    def update_last_name(self):
        if self.new_last_name:
            return self.new_last_name
        return None

    def update_witness(self):
        if self.new_witness_name:
            self.subject_consent.witness_name = self.new_witness_name

    def update_name_and_initials(self, enrollment_checklist):
        """Updates the firstname, lastname, initals and verifies the initials are valid."""
        first_name = self.new_first_name if self.new_first_name else self.subject_consent.first_name
        self.subject_consent.household_member.first_name = first_name
        self.subject_consent.first_name = first_name
        last_name = self.new_last_name if self.new_last_name else self.subject_consent.last_name
        self.subject_consent.household_member.last_name = last_name
        self.subject_consent.last_name = last_name
        initials = self.update_initials(first_name, last_name)
        self.subject_consent.household_member.initials = initials
        self.subject_consent.initials = initials
        enrollment_checklist.initials = initials

    class Meta:
        abstract = True


class CorrectConsent(BaseCorrectConsent, BaseSyncUuidModel):

    """A model linked to the subject consent to record corrections."""

    subject_consent = models.OneToOneField(SubjectConsent)

    objects = CorrectConsentManager()

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.subject_consent)

    def natural_key(self):
        return self.subject_consent.natural_key()

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
