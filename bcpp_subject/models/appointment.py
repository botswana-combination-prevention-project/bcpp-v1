from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    class Meta(AppointmentModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
