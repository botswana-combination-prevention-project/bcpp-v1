from django.db.models.signals import Signal, post_save
from bhp_consent.models import BaseConsentedUuidModel


class BaseAppointmentHelperModel (BaseConsentedUuidModel):

    """ Base for models that may be trigger the creation of appointments such as registration models models that need a key to RegisteredSubject.

    Such models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments.

    """

    def deserialize_prep(self):
        Signal.disconnect(post_save, None, weak=False, dispatch_uid="prepare_appointments_on_post_save")

    def deserialize_post(self):
        Signal.connect(post_save, None, weak=False, dispatch_uid="prepare_appointments_on_post_save")

    def pre_prepare_appointments(self):
        """Users may override to add functionality before creating appointments."""
        return None

    def post_prepare_appointments(self):
        """Users may override to add functionality after creating appointments."""
        return None

    def prepare_appointments(self):
        """Creates all appointments linked to this instance.

        Calls :func:`pre_prepare_appointments` and :func:`post_prepare_appointments`.

        .. seealso:: :class:`appointment_helper.AppointmentHelper`. """
        self.pre_prepare_appointments()
        from bhp_appointment_helper.classes import AppointmentHelper
        AppointmentHelper().create_all(self.registered_subject, self.__class__.__name__.lower())
        self.post_prepare_appointments()

    class Meta:
        abstract = True
