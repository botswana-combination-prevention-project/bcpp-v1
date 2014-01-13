from django.db import models
from django.conf import settings

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO
from edc.subject.consent.models import BaseConsent
from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import COMMUNITIES

from .clinic_off_study_mixin import ClinicOffStudyMixin


# declare abstract base class
class BaseClinicConsent(ClinicOffStudyMixin, BaseConsent):

    registered_subject = models.ForeignKey(RegisteredSubject,  # this also updates from household_member in save()
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

    # see additional mixin fields below

    def get_subject_type(self):
        return 'subject'

    def get_site_code(self):
        return settings.SITE_CODE

    def get_registered_subject(self):
        return self.registered_subject

    def dispatch_container_lookup(self, using=None):
        return ''

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
