from datetime import date
from dateutil.relativedelta import relativedelta

from edc.subject.appointment.models import Holiday

from ..choices import REFERRAL_CODES

from ..utils import next_clinic_date


class SubjectReferralApptHelper(object):
    """A class to determine the referral appointment date."""

    def __init__(self, referral_code, scheduled_appt_date=None):
        self._referral_appt_date = None
        self.referral_code = None
        self.scheduled_appt_date = None
        self.referral_clinic_type = 'IDCC'  # default
        if referral_code not in [item[0] for item in REFERRAL_CODES]:
            raise TypeError('Invalid referral code. Got {0}'.format(referral_code))
        self.referral_code = referral_code
        if date.today() > scheduled_appt_date:
            raise TypeError('Expected future date for scheduled appointment, Got {0}'.format(scheduled_appt_date))
        else:
            rdelta = relativedelta(scheduled_appt_date, date.today())
            if rdelta.years == 0 and ((rdelta.months == 1 and rdelta.days == 0) or (rdelta.months == 0)):
                self.scheduled_appt_date = scheduled_appt_date

    def __repr__(self):
        return 'SubjectReferralApptHelper({0.referral_code!r})'.format(self)

    def __str__(self):
        return '({0.referral_code!r})'.format(self)

    @property
    def referral_appt_date(self):
        """Returns the calculated referral appointment date based on the referral code and a scheduled appointment date."""
        if 'POS!-PR' in self.referral_code:
            # schedule next ANC day
            self._referral_appt_date = self.next_anc_date
            self.referral_clinic_type = 'ANC'
        elif 'POS!' in self.referral_code and not self.referral_code == 'POS!-PR':
            # schedule next IDCC day
            self._referral_appt_date = self.next_idcc_date
            self.referral_clinic_type = 'IDCC'
        elif 'MASA' in REFERRAL_CODES:
            # next idcc date or schedule appt
            self._referral_appt_date = self.scheduled_appt_date or self.next_idcc_date
            self.referral_clinic_type = 'IDCC'
        elif '-PR' in REFERRAL_CODES or '-AN' in REFERRAL_CODES:
            # next ANC date or schedule appt
            self._referral_appt_date = self.scheduled_appt_date or self.next_anc_date
            self.referral_clinic_type = 'ANC'
        elif 'SMC' in REFERRAL_CODES and self.intervention_community:
            # next SMC date or schedule appt
            self._referral_appt_date = self.scheduled_appt_date or self.next_smc_date
            self.referral_clinic_type = 'SMC'
        elif 'SMC' in REFERRAL_CODES and not self.intervention_community:
            # next SMC-ECC date or schedule appt
            self._referral_appt_date = self.scheduled_appt_date or self.next_smc_date
            self.referral_clinic_type = 'SMC-ECC'
        else:
            # default everyone else to the next IDCC date
            self._referral_appt_date = self.next_idcc_date()
            self.referral_clinic_type = 'IDCC'
        return self._referral_appt_date

    @property
    def next_idcc_date(self):
        next_idcc_date = None
        return next_idcc_date

    @property
    def next_smc_date(self):
        next_smc_date = None
        return next_smc_date

    @property
    def next_anc_date(self):
        next_anc_date = None
        return next_anc_date
