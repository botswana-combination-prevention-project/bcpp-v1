from django.db import models
from django.db.models import get_app, get_models
from registered_subject import RegisteredSubject
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_visit_tracking.models.base_visit_tracking import BaseVisitTracking
from bhp_appointment_helper.classes import AppointmentHelper


class BaseRegisteredSubjectModel (BaseUuidModel):

    """ Base model for models that need a key to RegisteredSubject.

    Such models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments. Other instances may be Additional
    forms which are link to a subject but not a time point (for example,
    a Death model or OffStudy model (see also AdditionalEntryBucket)

    Use this along with BaseRegisteredSubjectModelAdmin()

    """
    registered_subject = models.OneToOneField(RegisteredSubject)

    def get_visit_model(self, instance):
        for model in get_models(get_app(instance._meta.app_label)):
            if isinstance(model(), BaseVisitTracking):
                return model
        raise TypeError('Unable to determine the visit model from instance {0} for app {1}'.format(instance._meta.model_name, instance._meta.app_label))

    def save(self, *args, **kwargs):

        super(BaseRegisteredSubjectModel, self).save(*args, **kwargs)
        if not kwargs.get('suppress_autocreate_on_deserialize', False):
            AppointmentHelper().create_all(self.registered_subject, self.__class__.__name__.lower())

    class Meta:
        abstract = True
