from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge

from apps.bcpp.choices import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HicEnrollment (BaseScheduledVisitModel):

    hic_permission = models.CharField(
        verbose_name="Is it okay for the project to visit you every year for the next three years for further questions and testing?",
        max_length=25,
        choices=YES_NO,
        help_text='If \'No\', subject is not eligible.'
        )

    permanent_resident = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text='From Residency and Mobility. Eligible if Yes.'
        )

    intend_residency = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text='From Residency and Mobility. Eligible if Yes.'
        )

    hiv_status_today = models.CharField(
        max_length=50,
        help_text="From Today's HIV Result. Eligible if Negative.",
        # editable=False,
        )

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        default=None,
        # editable=False,
        help_text=_("Format is YYYY-MM-DD. From Subject Consent."),
        )

    household_residency = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text='Is Participant a Household Member. Eligible if Yes.'
        )

    citizen_or_spouse = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text=("From Subject Consent. Is participant a citizen, or married to citizen with a valid marriage certificate?"),
        )

    locator_information = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text=("From Subject Locator. Is the locator form filled and all necessary contact information collected?"),
        )

    consent_datetime = models.DateTimeField("Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        # editable=False,
        help_text=("From Subject Consent.")
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.hic_permission.lower() == 'yes':
            #Only enforce the criteria if subjectt agrees to enroll in HIC
            self.permanent_resident = self.is_permanent_resident()
            self.intend_residency = self.is_intended_residency()
            self.hiv_status_today = self.get_hiv_status_today()
            dob, consent_datetime = self.get_dob_consent_datetime()
            self.dob = dob
            self.consent_datetime = consent_datetime
            self.household_residency = self.is_household_residency()
            self.citizen_or_spouse = self.is_citizen_or_spouse()
            self.locator_information = self.is_locator_information()
        super(HicEnrollment, self).save(*args, **kwargs)

    def is_permanent_resident(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import ResidencyMobility
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].permanent_resident.lower() == 'yes':
                return True
            else:
                raise exception_cls('Please review \'residency_mobility\' in ResidencyMobility form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def is_intended_residency(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import ResidencyMobility
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].permanent_resident.lower() == 'yes':
                return True
            else:
                raise exception_cls('Please review \'intend_residency\' in ResidencyMobility form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def get_hiv_status_today(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import HivResult
        hiv_result = HivResult.objects.filter(subject_visit=self.subject_visit)
        if hiv_result.exists():
            if hiv_result[0].hiv_result.lower() == 'neg':
                return 'NEG'
            else:
                raise exception_cls('Please review \'hiv_result\' in Today\'s Hiv Result form before proceeding with this one.')
        else:
            raise exception_cls('Please fill Today\'s Hiv Result form before proceeding with this one.')

    def get_dob_consent_datetime(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import SubjectConsent
        subject_consent = SubjectConsent.objects.filter(household_member=self.subject_visit.household_member)
        if subject_consent.exists():
            if subject_consent[0].dob and subject_consent[0].consent_datetime:
                return (subject_consent[0].dob, subject_consent[0].consent_datetime)
            else:
                raise exception_cls('Please review \'dob\' and \'consent_datetime\' in SubjectConsent form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectConsent form before proceeding with this one.')

    def is_household_residency(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if self.subject_visit.household_member:
            return True
        else:
            raise exception_cls('This form has to be attached by to a household member. Currently it is not.')

    def is_citizen_or_spouse(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import SubjectConsent
        subject_consent = SubjectConsent.objects.filter(household_member=self.subject_visit.household_member)
        if subject_consent.exists():
            if ((subject_consent[0].citizen.lower() == 'yes') or (subject_consent[0].legal_marriage.lower() == 'yes' and subject_consent[0].marriage_certificate.lower() == 'yes')):
                return True
            else:
                raise exception_cls('Please review \'citizen\', \'legal_marriage\' and \'marriage_certificate\' in SubjectConsent form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectConsent form before proceeding with this one.')

    def is_locator_information(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import SubjectLocator
        subject_locator = SubjectLocator.objects.filter(subject_visit=self.subject_visit)
        if subject_locator.exists():
            if subject_locator[0].subject_cell or subject_locator[0].subject_cell_alt or subject_locator[0].subject_phone:
                return True
            else:
                raise exception_cls('Please review \'subject_cell\', \'subject_cell_alt\' and \'subject_phone\' in SubjectLocator form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectLocator form before proceeding with this one.')

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hic Enrollment"
        verbose_name_plural = "Hic Enrollment"
