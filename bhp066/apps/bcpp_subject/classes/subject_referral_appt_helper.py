from django.core.exceptions import ValidationError

from edc.constants import NOT_REQUIRED, KEYED
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.appointment.models import Holiday

from apps.bcpp_household_member.models import EnrollmentChecklist

from ..choices import REFERRAL_CODES
from ..models import (SubjectConsent, ResidencyMobility, Circumcision, ReproductiveHealth, SubjectLocator)
from ..utils import next_clinic_date

from .subject_status_helper import SubjectStatusHelper
from collections import namedtuple


class SubjectAppointmentHelper(SubjectStatusHelper):
    """A class to determine the referral appointment date."""

    @property
    def referral_appt_date(self):
        return self._referral_appt_date
