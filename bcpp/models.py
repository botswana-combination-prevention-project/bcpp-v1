from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_base.model.models import BaseUuidModel


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'bcpp'
