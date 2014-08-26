from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError

from edc.map.classes.controller import site_mappers
# from edc.subject.appointment.models import Holiday

from ..choices import REFERRAL_CODES

from ..utils import next_clinic_date


class SubjectReferralApptHelper(object):
    """A class to determine the referral appointment date.

    The referral code will determine the correct clinic,
    IDCC, ANC, SMC, SMC-ECC, to pass to the method
    :func:`next_appt_date.
    """

    def __init__(self, community_code, referral_code, base_date=None, scheduled_appt_date=None,
                 community_clinic_days=None, intervention_communities=None):
        self._base_date = base_date or datetime.today()  # should come from the user as today's date??
        self._intervention_communities = intervention_communities
        self._referral_code = None
        self._scheduled_appt_date = scheduled_appt_date
        self.community_code = community_code
        self.original_scheduled_appt_date = scheduled_appt_date
        self.referral_code = referral_code
        try:
            self.clinic_days = community_clinic_days.get(self.referral_clinic_type)
        except AttributeError:
            self.clinic_days = site_mappers.get_current_mapper().clinic_days.get(self.referral_clinic_type)

    def __repr__(self):
        return 'SubjectReferralApptHelper({0.referral_code!r})'.format(self)

    def __str__(self):
        return '({0.referral_code!r})'.format(self)

    @property
    def referral_appt_datetime(self):
        """Returns a referral_appt_datetime which is conditionally
        a given scheduled date or a calculated date."""
        referral_appt_datetime = None
        if 'SMC' in self.referral_code:
            referral_appt_datetime = self.smc_appt_datetime
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
        return referral_appt_datetime or next_clinic_date(self.clinic_days,
                                                          self.base_datetime)

    @property
    def referral_clinic_type(self):
        """Returns the calculated referral appointment date based on
        the referral code and a scheduled appointment date."""
        clinic_type = None
        if self.referral_code in ['POS!-HI', 'POS!-LO', 'POS#-HI', 'POS#-LO']:
            clinic_type = 'IDCC'
        elif 'MASA' in self.referral_code:
            clinic_type = 'IDCC'
        elif 'TST-HIV' in self.referral_code:
            clinic_type = 'VCT'
        elif 'TST-CD4' in self.referral_code:
            clinic_type = 'IDCC'
        elif '-PR' in self.referral_code or '-AN' in self.referral_code:
            clinic_type = 'ANC'
        elif 'SMC' in self.referral_code:
            clinic_type = 'SMC'
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

#     @property
#     def intervention_community(self):
#         """Returns a True if this community is an intervention community
#         (CPC) otherwise False."""
#         try:
#             # this is just for testing -- can pass a list of community codes
#             intervention_community = True if self.community_code in self._intervention_communities else False
#         except TypeError:
#             intervention_community = site_mappers.get_current_mapper().intervention
#         return intervention_community

    @property
    def scheduled_appt_datetime(self):
        """Returns a datetime as long as the date is within 1 month
        of today otherwise leaves the date as None."""
        scheduled_appt_datetime = None
        if self._scheduled_appt_date:
            scheduled_appt_datetime = datetime(self._scheduled_appt_date.year,
                                               self._scheduled_appt_date.month,
                                               self._scheduled_appt_date.day, 7, 30, 0)
            if self.base_datetime > scheduled_appt_datetime:
                raise ValidationError('Expected future date for scheduled appointment, '
                                      'Got {0}'.format(self._scheduled_appt_date))
            rdelta = relativedelta(scheduled_appt_datetime, self.base_datetime)
            if rdelta.years == 0 and ((rdelta.months == 1 and rdelta.days == 0) or (rdelta.months == 0)):
                scheduled_appt_datetime = next_clinic_date(self.clinic_days,
                                                           scheduled_appt_datetime,
                                                           allow_same_day=True)
        return scheduled_appt_datetime

    @property
    def base_datetime(self):
        """Returns the base date as a datetime."""
        return datetime(self._base_date.year, self._base_date.month, self._base_date.day, 7, 30, 0)

    @property
    def masa_appt_datetime(self):
        """Returns a date as long as the date is within 1 month
        of today otherwise returns two weeks from base."""
        return next_clinic_date(self.clinic_days,
                                self.base_datetime + relativedelta(weeks=2))

    @property
    def smc_appt_datetime(self):
        """Returns a datetime that is either the smc start date or the
        next smc clinic day depending on whether today id before or
        after smc_start_date,"""
        smc_appt_datetime = datetime(self.clinic_days.start_date.year, self.clinic_days.start_date.month, self.clinic_days.start_date.day, 7, 30, 0)
        if self.base_datetime > smc_appt_datetime:
            smc_appt_datetime = next_clinic_date(self.clinic_days,
                                                 self.base_datetime)
        else:
            smc_appt_datetime = next_clinic_date(self.clinic_days,
                                                 self.clinic_days.start_date,
                                                 allow_same_day=True)
        return smc_appt_datetime
