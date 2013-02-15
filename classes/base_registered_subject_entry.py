from django.core.exceptions import FieldError
from bhp_registration.models import BaseRegisteredSubjectModel
from base_entry import BaseEntry


class BaseRegisteredSubjectEntry(BaseEntry):

    def __init__(self):
        self._registered_subject_instance = None
        super(BaseRegisteredSubjectEntry, self).__init__()

    def _set_registered_subject_instance(self, value=None):
        if value:
            self._registered_subject_instance = value
        else:
            raise TypeError('Attribute _registered_subject_instance cannot be None')

    def get_registered_subject_instance(self):
        if not self._registered_subject_instance:
            self._set_registered_subject_instance()
        return self._registered_subject_instance

    def set_target_model_base_cls(self):
        self._target_model_base_cls = BaseRegisteredSubjectModel

    def set_target_model_cls_with_content_type(self, value=None):
        self.set_target_model_cls(self.get_bucket_model_instance().content_type_map.model_class())

    def set_target_model_instance(self, target_model_instance=None):
        """ Sets the instance of the target model class if it can using the registered_subject."""
        self._target_model_instance = None
        if target_model_instance:
            self._target_model_instance = target_model_instance
            self.set_target_model_cls_with_content_type(self._target_model_instance.__class__)
        elif self.get_registered_subject_instance():
            try:
                if self.get_target_model_cls().objects.filter(**{self.get_visit_model_fieldname(): self.get_visit_model_instance()}).exists():
                    self._target_model_instance = self.get_target_model_cls().objects.get(**{self.get_visit_model_fieldname(): self.get_visit_model_instance()})
            except FieldError as e:
                raise FieldError('Field {0} does not exist in model class {1}. Got {2}'.format(self.get_visit_model_fieldname(), self.get_target_model_cls(), e))
            except:
                raise
        else:
            pass
