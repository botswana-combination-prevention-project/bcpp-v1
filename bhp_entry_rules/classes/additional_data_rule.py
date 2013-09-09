import logging
from bhp_entry.classes import AdditionalEntry
from bhp_entry.models import AdditionalEntryBucket
from base_rule import BaseRule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class AdditionalDataRule(BaseRule):

    def set_bucket_cls(self):
        self._bucket_cls = AdditionalEntryBucket

    def set_entry_cls(self):
        self._entry_cls = AdditionalEntry

    def get_action_list(self):
        return ['required', 'not_required']

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreignkey that points to registered subjectl."""
        self._filter_fieldname = 'appointment__registered_subject'

    def set_source_model_instance(self, source_model_instance=None):
        """Always sets source_model_instance to an instance of visit model. """
        self._source_model_instance = self.get_visit_model_instance()

    def set_target_bucket_instance_id(self):
        """Sets the bucket_instance_id for the target model"""
        self._target_bucket_instance_id = None
        if self.get_visit_model_instance():
            if self.get_bucket_cls().objects.filter(
                    content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_visit_model_instance().appointment.registered_subject).exists():
                bucket_instance_map = self.get_bucket_cls().objects.values('id').get(
                    content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_visit_model_instance().appointment.registered_subject)
                self._target_bucket_instance_id = bucket_instance_map.get('id')

    def evaluate(self):
        """ Evaluate predicate and add/remove an entry from bucket class."""
        logger.debug('Evaluating rule {0} targeted for {1}.'.format(self, self.get_target_model_cls()._meta.object_name))
        predicate = self.get_predicate()
        if predicate:
            if eval(predicate):
                action = self.get_consequent_action()
            else:
                action = self.get_alternative_action()
            if self.is_valid_action(action):
                if not self.get_target_bucket_instance_id() and action.lower() == 'required':
                    EntryCls = self.get_entry_cls()
                    entry = EntryCls()
                    entry.add_from_rule(
                        self.__repr__(),
                        self.get_visit_model_instance(),
                        self.get_target_content_type_map())
                if self.get_target_bucket_instance_id() and action.lower() == 'not_required':
                    EntryCls = self.get_entry_cls()
                    entry = EntryCls()
                    entry.remove_from_rule(
                        self.__repr__(),
                        self.get_target_model_cls(),
                        self.get_visit_model_instance(),
                        self.get_target_content_type_map())
