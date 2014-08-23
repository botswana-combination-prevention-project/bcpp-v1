from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError

# from edc.subject.appointment.models import Holiday

from ..choices import REFERRAL_CODES

from ..utils import next_clinic_date


class SubjectReferralApptHelper(object):
    """A class to determine the referral appointment date.

    The referral code will determine the correct clinic,
    IDCC, ANC, SMC, SMC-ECC, to pass to the method
    :func:`next_appt_date.
    """

    def __init__(self, community_code, referral_code, base_date=None, scheduled_appt_date=None, smc_start_date=None,
                 clinic_days=None, intervention_communities=None):
        self._referral_code = None
        self._scheduled_appt_datetime = None
        self.community_code = community_code
        self.intervention_communities = intervention_communities or settings.INTERVENTION_COMMUNITIES
        self.referral_code = referral_code
        self.base_datetime = base_date or datetime.today()  # should come from the user as today's date??
        self.original_scheduled_appt_date = scheduled_appt_date
        self.scheduled_appt_datetime = scheduled_appt_date
        self.smc_start_date = smc_start_date or settings.SMC_START_DATE
        self.clinic_days = clinic_days or settings.CLINIC_DAYS

    def __repr__(self):
        return 'SubjectReferralApptHelper({0.referral_code!r})'.format(self)

    def __str__(self):
        return '({0.referral_code!r})'.format(self)

    @property
    def referral_appt_datetime(self):
        """Returns a referral_appt_datetime which is conditionally
        a given scheduled date or a calculated date."""
        referral_appt_datetime = None
        if 'SMC' in self.clinic_type:
            referral_appt_datetime = self.smc_appt_datetime(self.smc_start_date)
        elif self.referral_code == 'MASA-DF':
            pass  # will be next clinic date and will ignore a scheduled_appt_date
        else:
            try:
                if self.scheduled_appt_datetime <= self.base_datetime + relativedelta(months=1):
                    referral_appt_datetime = self.scheduled_appt_datetime
            except TypeError as e:
                if "can't compare datetime.datetime to NoneType" not in e:
                    raise TypeError(e)
                pass
            if not referral_appt_datetime and 'MASA' in self.referral_code:
                referral_appt_datetime = self.masa_appt_datetime
        return referral_appt_datetime or next_clinic_date(self.community_code,
                                                          self.clinic_type,
                                                          self.base_datetime)

    @property
    def clinic_type(self):
        """Returns the calculated referral appointment date based on
        the referral code and a scheduled appointment date."""
        clinic_type = None
        if 'POS!-PR' in self.referral_code:
            clinic_type = 'ANC'
        elif 'POS!' in self.referral_code and not self.referral_code == 'POS!-PR':
            clinic_type = 'IDCC'
        elif 'MASA' in self.referral_code:
            clinic_type = 'IDCC'
        elif 'TST-HIV' in self.referral_code:
            clinic_type = 'IDCC'
        elif 'TST-CD4' in self.referral_code:
            clinic_type = 'IDCC'
        elif '-PR' in self.referral_code or '-AN' in self.referral_code:
            clinic_type = 'ANC'
        elif 'SMC' in self.referral_code and self.intervention_community:
            clinic_type = 'SMC'
        elif 'SMC' in self.referral_code and not self.intervention_community:
            clinic_type = 'SMC-ECC'
        return clinic_type

    @property
    def referral_code(self):
        """Returns the referral code."""
        return self._referral_code

    @referral_code.setter
    def referral_code(self, referral_code):
        """Sets the referral code after confirming the code is
        valid or ''."""
        if referral_code not in [item[0] for item in REFERRAL_CODES] + [None, '']:
            raise TypeError('Invalid referral code. Got {0}'.format(referral_code))
        self._referral_code = referral_code

    @property
    def intervention_community(self):
        """Returns a True if this community is an intervention community
        (CPC) otherwise False."""
        try:
            intervention_community = self.intervention_communities[
                self.intervention_communities.index(self.community_code)]
        except ValueError:
            intervention_community = False
        return intervention_community

    @property
    def scheduled_appt_datetime(self):
        """Returns the scheduled appt date as a datetime."""
        return self._scheduled_appt_datetime

    @scheduled_appt_datetime.setter
    def scheduled_appt_datetime(self, scheduled_appt_date):
        """Sets a date as long as the date is within 1 month
        of today otherwise leaves the date as None."""
        self._scheduled_appt_datetime = None
        if scheduled_appt_date:
            scheduled_appt_datetime = datetime(scheduled_appt_date.year,
                                               scheduled_appt_date.month,
                                               scheduled_appt_date.day, 7, 30, 0)
            if self.base_datetime > scheduled_appt_datetime:
                raise ValidationError('Expected future date for scheduled appointment, '
                                      'Got {0}'.format(scheduled_appt_date))
            rdelta = relativedelta(scheduled_appt_datetime, self.base_datetime)
            if rdelta.years == 0 and ((rdelta.months == 1 and rdelta.days == 0) or (rdelta.months == 0)):
                self._scheduled_appt_datetime = next_clinic_date(self.community_code,
                                                                 self.clinic_type,
                                                                 scheduled_appt_datetime,
                                                                 allow_same_day=True)

    @property
    def base_datetime(self):
        """Returns the base date as a datetime."""
        return self._base_datetime

    @base_datetime.setter
    def base_datetime(self, base_datetime):
        """Sets base date, usually today, as a datetime."""
        self._base_datetime = datetime(base_datetime.year, base_datetime.month, base_datetime.day, 7, 30, 0)

    @property
    def masa_appt_datetime(self):
        """Returns a date as long as the date is within 1 month
        of today otherwise returns two weeks from base."""
        return next_clinic_date(self.community_code,
                                self.clinic_type,
                                self.base_datetime + relativedelta(weeks=2))

    def smc_appt_datetime(self, smc_appt_date):
        """Returns a datetime that is either the smc start date or the
        next smc clinic day depending on whether today id before or
        after smc_start_date,"""
        smc_appt_datetime = datetime(smc_appt_date.year, smc_appt_date.month, smc_appt_date.day, 7, 30, 0)
        if self.base_datetime > smc_appt_datetime:
            smc_appt_datetime = next_clinic_date(self.community_code,
                                                 self.clinic_type,
                                                 self.base_datetime)
        return smc_appt_datetime
