from datetime import datetime, date
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

    def __init__(self, community_code, referral_code, today_date=None, scheduled_appt_date=None, smc_start_date=None,
                 clinic_days=None, intervention_communities=None):
        self.community_code = community_code
        if referral_code not in [item[0] for item in REFERRAL_CODES] + [None, '']:
            raise TypeError('Invalid referral code. Got {0}'.format(referral_code))
        self.referral_code = referral_code
        self.today_date = today_date or date.today()  # should come from the user as today's date??
        self._scheduled_appt_date = scheduled_appt_date
        self.smc_start_date = smc_start_date or settings.SMC_START_DATE
        self.clinic_days = clinic_days or settings.CLINIC_DAYS
        intervention_communities = intervention_communities or settings.INTERVENTION_COMMUNITIES
        try:
            self.intervention_community = intervention_communities[intervention_communities.index(self.community_code)]
        except ValueError:
            self.intervention_community = False

    def __repr__(self):
        return 'SubjectReferralApptHelper({0.referral_code!r})'.format(self)

    def __str__(self):
        return '({0.referral_code!r})'.format(self)

    @property
    def referral_appt_datetime(self):
        """Returns a referral_appt_datetime which is conditionally
        a given scheduled date or a calculated date."""
        referral_appt_datetime = None
        try:
            if self.scheduled_appt_date <= self.today_date + relativedelta(months=1):
                referral_appt_datetime = datetime(self.scheduled_appt_date.year,
                                                  self.scheduled_appt_date.month,
                                                  self.scheduled_appt_date.day, 7, 30, 0)
        except TypeError:
            pass
#         if referral_appt_datetime:
#             # check falls on an clinic day, if not fail
        return referral_appt_datetime or next_clinic_date(self.community_code,
                                                          self.clinic_type,
                                                          today=self.today_date,
                                                          referral_code=self.referral_code)

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
    def scheduled_appt_date(self):
        """Returns a date as long as the date is within 1 month
        of today otherwise returns None."""
        try:
            if self.today_date > self._scheduled_appt_date:
                raise ValidationError('Expected future date for scheduled appointment, Got {0}'.format(self._scheduled_appt_date))
        except TypeError:  # scheduled_appt_date == None
            pass
        rdelta = relativedelta(self._scheduled_appt_date, self.today_date)
        if rdelta.years == 0 and ((rdelta.months == 1 and rdelta.days == 0) or (rdelta.months == 0)):
            return self._scheduled_appt_date
        return None
