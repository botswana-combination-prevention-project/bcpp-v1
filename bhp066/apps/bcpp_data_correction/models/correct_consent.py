from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from apps.bcpp_subject.models import SubjectConsent
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import EnrollmentChecklist


from edc.choices.common import GENDER_UNDETERMINED
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.core.crypto_fields.fields import EncryptedFirstnameField, EncryptedCharField
from edc.core.crypto_fields.fields import EncryptedLastnameField
from edc.choices.common import YES_NO
from edc.device.dispatch.models import BaseDispatchSyncUuidModel


class CorrectConsent(BaseDispatchSyncUuidModel):

    """ Consent models should be subclasses of this """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
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
    initials = EncryptedCharField(
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

    gender = models.CharField(
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

    may_store_samples = models.CharField(
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

    def save(self, *args, **kwargs):
        consent_form_dict = {
                'subject_identifier': self.subject_identifier,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'initials': self.initials,
                'dob': self.dob,
                'gender': self.gender,
                'guardian_name': self.guardian_name,
                'is_literate': self.is_literate,
                'may_store_samples': self.may_store_samples}
        consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        household_member = HouseholdMember.objects.get(id=consent.household_member_id)
        erollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        erollment_checklist.update_values = True
        erollment_checklist.save()
        household_member_fields = []
        consent_fields = []
        enrollment_fields = []
        for field in HouseholdMember._meta.fields:
            household_member_fields.append(field.name)
        for field in EnrollmentChecklist._meta.fields:
            enrollment_fields.append(field.name)
        for field in SubjectConsent._meta.fields:
            consent_fields.append(field.name)

        for key, value in consent_form_dict.iteritems():
            if value:
                if key in household_member_fields:
                    household_member.key = value
                    household_member.save()
                if key == 'dob':
                    age_in_years = relativedelta(date.today(), self.dob).years
                    household_member.age_in_years = age_in_years
                    household_member.save()
        household_member = HouseholdMember.objects.get(id=consent.household_member_id)
        erollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        for key, value in consent_form_dict.iteritems():
            if value:
                if key in enrollment_fields:
                    erollment_checklist.key = value
                    erollment_checklist.save()
        consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        for key, value in consent_form_dict.iteritems():
            if value:
                if key in consent_fields and not key == 'subject_identifier':
                    consent.key = value
                    consent.save()
        super(CorrectConsent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_data_correction'

