import re
import uuid

from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings

from edc.core.identifier.classes import SubjectIdentifier
from edc.device.sync.models import BaseSyncUuidModel
from edc.map.classes import site_mappers
from edc_base.audit_trail import AuditTrail
from edc_consent.models.fields import (
    ReviewFieldsMixin, SampleCollectionFieldsMixin, PersonalFieldsMixin,
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin

from .clinic_off_study_mixin import ClinicOffStudyMixin
from bhp066.apps.bcpp_subject.models.subject_consent import BaseBaseSubjectConsent


class ClinicConsent(BaseBaseSubjectConsent, ClinicOffStudyMixin, PersonalFieldsMixin,
                    VulnerabilityFieldsMixin, SampleCollectionFieldsMixin, ReviewFieldsMixin,
                    IdentityFieldsMixin, CitizenFieldsMixin, BaseSyncUuidModel):
    """A model completed by the user to capture the ICF."""
    lab_identifier = models.CharField(
        verbose_name=("lab allocated identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    htc_identifier = models.CharField(
        verbose_name=("HTC Identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    pims_identifier = models.CharField(
        verbose_name=("PIMS identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = site_mappers.get_current_mapper().map_area
        # self.clinic_subject_identifier()
        super(ClinicConsent, self).save(*args, **kwargs)

    def is_dispatchable_model(self):
        return False

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
