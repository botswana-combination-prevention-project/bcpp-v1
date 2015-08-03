from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge

from apps.bcpp.choices import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel
from ..models import ElisaHivResult


class HicEnrollment (BaseScheduledVisitModel):

    hic_permission = models.CharField(
        verbose_name=_('Is it okay for the project to visit you every year for '
                       'the next three years for further questions and testing?'),
        max_length=25,
        choices=YES_NO,
        help_text=_('If \'No\', subject is not eligible.')
        )

    permanent_resident = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text=_('From Residency and Mobility. Eligible if Yes.')
        )

    intend_residency = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text=_('From Residency and Mobility. Eligible if No.')
        )

    hiv_status_today = models.CharField(
        max_length=50,
        help_text=_("From Today's HIV Result. Eligible if Negative."),
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
        null=True,
        blank=True,
        help_text=_('Is Participant a Household Member. Eligible if Yes.')
        )

    citizen_or_spouse = models.NullBooleanField(
        default=None,
        # editable=False,
        help_text=_('From Subject Consent. Is participant a citizen, or married to citizen '
                    'with a valid marriage certificate?'),
        )

    locator_information = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text=_('From Subject Locator. Is the locator form filled and all '
                    'necessary contact information collected?'),
        )

    consent_datetime = models.DateTimeField("Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        # editable=False,
        help_text=_("From Subject Consent.")
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.hic_permission.lower() == 'yes':
            # Only enforce the criteria if subjectt agrees to enroll in HIC
            self.permanent_resident = self.is_permanent_resident()
            self.intend_residency = self.is_intended_residency()
            self.household_residency = self.is_household_residency()
            self.locator_information = self.is_locator_information()
            self.citizen_or_spouse = self.is_citizen_or_spouse()
            self.hiv_status_today = self.get_hiv_status_today()
        update_fields = kwargs.get('update_fields')
        if not update_fields:
            dob, consent_datetime = self.get_dob_consent_datetime()
            self.dob = dob
            self.consent_datetime = consent_datetime
        super(HicEnrollment, self).save(*args, **kwargs)

    def is_permanent_resident(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import ResidencyMobility
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].permanent_resident.lower() == 'yes':
                return True
            else:
                raise exception_cls('Please review \'residency_mobility\' in ResidencyMobility '
                                    'form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def is_intended_residency(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import ResidencyMobility
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].intend_residency.lower() == 'no':
                return True
            else:
                raise exception_cls('Please review \'intend_residency\' in ResidencyMobility '
                                    'form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def get_hiv_status_today(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import HivResult
        hiv_result = HivResult.objects.filter(subject_visit=self.subject_visit)
        elisa_result = ElisaHivResult.objects.filter(subject_visit=self.subject_visit)
        if hiv_result.exists():
            if (hiv_result[0].hiv_result.lower() == 'neg' or
                (elisa_result.exists() and elisa_result[0].hiv_result.lower() == 'neg')):
                return 'NEG'
            else:
                raise exception_cls('Please review \'hiv_result\' in Today\'s Hiv Result form or in Elisa Hiv Result'
                                    'before proceeding with this one.')
        else:
            raise exception_cls('Please fill Today\'s Hiv Result form before proceeding with this one.')

    def get_dob_consent_datetime(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import SubjectConsent
        subject_consent = SubjectConsent.objects.filter(subject_identifier=self.subject_visit.appointment.registered_subject.subject_identifier)
        if subject_consent.exists():
            if subject_consent[0].dob and subject_consent[0].consent_datetime:
                return (subject_consent[0].dob, subject_consent[0].consent_datetime)
            else:
                raise exception_cls('Please review \'dob\' and \'consent_datetime\' in SubjectConsent '
                                    'form before proceeding with this one.')
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
        try:
            subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_visit.appointment.registered_subject.subject_identifier)
            if ((subject_consent.citizen.lower() == 'yes') or (
                    subject_consent.legal_marriage.lower() == 'yes' and
                    subject_consent.marriage_certificate.lower() == 'yes')):
                return True
            else:
                raise exception_cls('Please review \'citizen\', \'legal_marriage\' and '
                                    '\'marriage_certificate\' in SubjectConsent for {}. Got {}, {}, {}'.format(
                                        subject_consent,
                                        subject_consent.citizen.lower(),
                                        subject_consent.legal_marriage.lower(),
                                        subject_consent.marriage_certificate.lower()
                                        ))
        except SubjectConsent.DoesNotExist:
            raise exception_cls('Please fill SubjectConsent form before proceeding with this one.')

    def is_locator_information(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        from ..models import SubjectLocator
        subject_locator = SubjectLocator.objects.filter(registered_subject=self.subject_visit.appointment.registered_subject)
        # At least some information to contact the person should be available
        if subject_locator.exists():
            if (subject_locator[0].subject_cell or
                    subject_locator[0].subject_cell_alt or
                    subject_locator[0].subject_phone or
                    subject_locator[0].mail_address or
                    subject_locator[0].physical_address or
                    subject_locator[0].subject_cell or
                    subject_locator[0].subject_cell_alt or
                    subject_locator[0].subject_phone or
                    subject_locator[0].subject_phone_alt or
                    subject_locator[0].subject_work_place or
                    subject_locator[0].subject_work_phone or
                    subject_locator[0].contact_physical_address or
                    subject_locator[0].contact_cell or
                    subject_locator[0].contact_phone):
                return True
            else:
                raise exception_cls('Please review SubjectLocator to ensure there is some '
                                    'way to contact the participant form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectLocator form before proceeding with this one.')

    def may_contact(self):
        if self.hic_permission == 'Yes':
            return '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        else:
            return '<img src="/static/admin/img/icon-no.gif" alt="False" />'
    may_contact.allow_tags = True

    def age(self):
        return relativedelta(self.consent_datetime.date(), self.dob).years
    age.allow_tags = True

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hic Enrollment"
        verbose_name_plural = "Hic Enrollment"
