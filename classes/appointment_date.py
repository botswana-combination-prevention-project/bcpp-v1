from datetime import datetime, timedelta
from bhp_appointment.models import Holiday, Configuration


class AppointmentDate(object):

    def get(self, appt_datetime, weekday=None):
        """ Gets the appointment date.

        For example, may be configured to be on the same day as the base, not on holiday, etc.

        Note, appt_datetime comes from the membership_form model method get_registration_datetime"""

        if not isinstance(appt_datetime, datetime):
            raise AttributeError('Expected parameter \'appt_datetime\' to be an instance of datetime')
        if weekday and self.use_same_weekday:
            appt_datetime = self.move_to_same_weekday(appt_datetime, weekday)
        appt_datetime = self.check_if_allowed_isoweekday(appt_datetime)
        appt_datetime = self.check_if_holiday(appt_datetime)
        # TODO:load balance to a day with fewer appointments
        return appt_datetime

    def change(self, best_appt_datetime, new_appt_datetime):
        """Checks if a changed appt datetime is OK."""
        td = best_appt_datetime - new_appt_datetime
        if abs(td.days()) <= 8 and new_appt_datetime >= datetime.today():
            retval = new_appt_datetime
        else:
            retval = None
        return retval

    @property
    def use_same_weekday(self):
        config = Configuration.objects.get_configuration()
        return config.use_same_weekday

    def check_if_allowed_isoweekday(self, appt_datetime):
        """ Checks if weekday is allowed, otherwise adjust forward or backward """
        # check if is allowable isoweekday based on integer value in
        # study_specific.allowed_iso_weekdays (e.g. 12345)
        allowed_iso_weekdays = [int(num) for num in str(self.get_appointment_configuration().allowed_iso_weekdays)]
        forward = appt_datetime
        while forward.isoweekday() not in allowed_iso_weekdays:
            forward = forward + timedelta(days=+1)
        backward = appt_datetime
        while backward.isoweekday() not in allowed_iso_weekdays:
            backward = backward + timedelta(days=-1)
        # which is closer to the original appt_datetime
        td_forward = abs(appt_datetime - forward)
        td_backward = abs(appt_datetime - backward)
        if td_forward <= td_backward:
            appt_datetime = forward
        else:
            appt_datetime = backward
        return appt_datetime

    def check_if_holiday(self, appt_datetime):
        """ Checks if appt_datetime lands on a holiday, if so, move forward """
        while appt_datetime.date() in [holiday.holiday_date for holiday in Holiday.objects.all()]:
            appt_datetime = appt_datetime + timedelta(days=+1)
            appt_datetime = self.check_if_allowed_isoweekday(appt_datetime)
        return appt_datetime

    def move_to_same_weekday(self, appt_datetime, weekday=1):
        """ Moves appointment if all appt to land in same day."""
        if weekday not in range(1, 8):
            raise ValueError('Weekday must be a number between 1-7, Got %s' % (weekday, ))
        # make all appointments land on the same isoweekday,
        # if possible as date may change becuase of holiday and/or iso_weekday checks below)
        forward = appt_datetime
        while not forward.isoweekday() == weekday:
            forward = forward + timedelta(days=+1)
        backward = appt_datetime
        while not backward.isoweekday() == weekday:
            backward = backward - timedelta(days=+1)
        # which is closer to the original appt_datetime
        td_forward = abs(appt_datetime - forward)
        td_backward = abs(appt_datetime - backward)
        if td_forward <= td_backward:
            appt_datetime = forward
        else:
            appt_datetime = backward
        return appt_datetime

        