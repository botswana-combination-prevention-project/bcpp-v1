from bhp066.apps.bcpp_household_member.models import MemberAppointment
from bhp066.apps.bcpp_household.utils.update_household_work_list import update_household_work_list


class CallHelper(object):

    def __init__(self, call_log_entry):
        self._member_appointment = None
        self._work_list = None
        self.call_log_entry = call_log_entry
        self.label = call_log_entry.call_log.label

    @property
    def call_log_entry(self):
        return self._call_log_entry

    @call_log_entry.setter
    def call_log_entry(self, value):
        self._member_appointment = None
        self._work_list = None
        self._call_log_entry = value

    @property
    def member_appointment(self):
        """Returns a member appointment after either updating or creating."""
        if not self._member_appointment:
            try:
                self._member_appointment = MemberAppointment.objects.get(
                    household_member=self.call_log_entry.call_log.household_member,
                    label=self.call_log_entry.call_log.label,
                )
                self._member_appointment.appt_date = self.call_log_entry.appt_date
                self._member_appointment.appt_status = 'new'
                self._member_appointment.time_of_day = self.call_log_entry.time_of_day
                self._member_appointment.time_of_week = self.call_log_entry.time_of_week
                self._member_appointment.user_modified = self.call_log_entry.user_modified,
                self._member_appointment.save()
            except MemberAppointment.DoesNotExist:
                self._member_appointment = MemberAppointment.objects.create(
                    household_member=self.call_log_entry.call_log.household_member,
                    appt_date=self.call_log_entry.appt_date,
                    survey=self.call_log_entry.call_log.survey,
                    label=self.call_log_entry.call_log.label,
                    time_of_day=self.call_log_entry.time_of_day,
                    time_of_week=self.call_log_entry.time_of_week,
                    is_confirmed=True,
                    user_created=self.call_log_entry.user_created,
                    user_modified=self.call_log_entry.user_modified,
                )
        return self._member_appointment

    @property
    def work_list(self):
        if not self._work_list:
            self._work_list = update_household_work_list(
                self.label, household_structure=self.call_log_entry.call_log.household_member.household_structure)
        return self._work_list
