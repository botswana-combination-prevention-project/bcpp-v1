from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import re

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO
from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc.subject.consent.models import BaseConsent
from edc.subject.registration.models import RegisteredSubject

from .clinic_off_study_mixin import ClinicOffStudyMixin

from apps.bcpp_subject.models import SubjectConsent
from .clinic_eligibility import ClinicEligibility
from apps.clinic.choices import COMMUNITIES


class BaseClinicConsent(ClinicOffStudyMixin, BaseAppointmentMixin, BaseConsent):

    registered_subject = models.ForeignKey(RegisteredSubject,
        editable=False,
        null=True,
        help_text='')

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text='Subject is a minor if aged 16-17. A guardian must be present for consent. HIV status may NOT be revealed in the household.')

    consent_signature = models.CharField(
        verbose_name=("The client has signed the consent form?"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        #default='Yes',
        help_text="If no, INELIGIBLE",
        )

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    have_htc_pims = models.CharField(
        verbose_name=("Does the participant have one of these identification numbers?"),
        max_length=30,
        choices=(
            ('barcode', 'Barcode Number'),
            ('Htc identifier', 'Htc identifier'),
            ('Pims identifier', 'Pims identifier'),
            ('Htc_Pims', 'Htc and Pims identifier'),
            ('Barcode_Pims', 'Barcode and Pims identifier'),
            ('None', 'None'),
            ),
        help_text="",
        )

    htc_pims_id = models.CharField(
        verbose_name=("Enter the HTC and or PIMS identifiers(comma separated)?"),
        max_length=50,
        null=True,
        blank=True,
        help_text="htc_identifier, pims_identifier",
        )

    def get_subject_type(self):
        return 'clinic'

    def get_site_code(self):
        return settings.SITE_CODE

#     def get_registered_subject(self):
#         return self.registered_subject

    def get_registration_datetime(self):
        return self.consent_datetime

    def update_registered_subject(self, **kwargs):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        using = kwargs.get('using', None)
        if re_pk.match(self.registered_subject.subject_identifier):
            self.registered_subject.subject_identifier = self.subject_identifier
        self.registered_subject.registration_status = 'CONSENTED'
        self.registered_subject.save(using=using)
        if self.subject_identifier != self.registered_subject.subject_identifier:
            raise TypeError('Subject identifier expected to be same as registered_subject subject_identifier. Got {0} != {1}'.format(self.subject_identifier, self.registered_subject.subject_identifier))

    def save(self, *args, **kwargs):
        if ClinicEligibility.objects.filter(dob=self.dob,
                                            gender=self.gender,
                                            first_name=self.first_name,
                                            initials=self.initials).exists():
            eligibility = ClinicEligibility.objects.get(dob=self.dob,
                                            gender=self.gender,
                                            first_name=self.first_name,
                                            initials=self.initials)
            eligibility.match_consent_values(eligibility)
            self.registered_subject = eligibility.registered_subject
        else:
            raise ValueError('Could not find a ClinicEligibility. Ensure \'DOB\', \'first_name\', \'gender\' and \'initials\' match those in ClinicEligibility.')
        self.validate_clinic_consent()
        self.update_registered_subject()
        super(BaseClinicConsent, self).save(*args, **kwargs)

    def validate_clinic_consent(self, subject_identifier=None):
        if SubjectConsent.objects.filter(first_name=self.first_name, last_name=self.last_name, identity=self.identity).exists():
            raise ValidationError('We cannot consent a subject twice! Subject was already consented in BHS.')

    def is_dispatchable_model(self):
        return False

#     def dispatch_container_lookup(self):
#         return None

    class Meta:
        abstract = True

# add Mixin fields to abstract class
for field in IdentityFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseClinicConsent._meta.fields]:
        field.contribute_to_class(BaseClinicConsent, field.name)

for field in ReviewAndUnderstandingFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseClinicConsent._meta.fields]:
        field.contribute_to_class(BaseClinicConsent, field.name)


# declare concrete class
class ClinicConsent(BaseClinicConsent):

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
