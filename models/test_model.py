from bhp_appointment.models import BaseAppointment
from base_appointment_mixin import BaseAppointmentMixin


class TestModel(BaseAppointment, BaseAppointmentMixin):

    class Meta:
        app_label = 'bhp_appointment_helper'
