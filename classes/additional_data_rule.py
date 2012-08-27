import logging
from bhp_entry.classes import AdditionalEntry
from bhp_entry.models import AdditionalEntryBucket
from bhp_visit_tracking.models import BaseVisitTracking
from rule import Rule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class AdditionalDataRule(Rule):

    def set_bucket_cls(self):
        self._bucket_cls = AdditionalEntryBucket

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreignkey that points to the visit model."""
        self._filter_fieldname = 'appointment__registered_subject'

    def set_source_model_instance(self, source_model_instance=None):
        """Sets to an instance of visit model, always, using a filter instance of registered subject """
        self._source_model_instance = self.get_visit_model_instance()

    def set_target_bucket_instance_id(self):
        """Sets the bucket_instance_id for the target models knowing that the filter
        instance is either an instance of BaseVisitTracking or RegisteredSubject.

        Might set to None if the current visit does not contain the target model, so users should check for None."""

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
        predicate = self.get_predicate()
        if predicate:
            if eval(predicate):
                action = self.get_consequent_action()
            else:
                action = self.get_alternative_action()
            if not self.get_target_bucket_instance_id() and action.lower() == 'required':
                additional_entry = AdditionalEntry()
                additional_entry.add_from_rule(
                    self.get_visit_model_instance(),
                    self.get_target_content_type_map())
            if self.get_target_bucket_instance_id() and action.lower() == 'notrequired'.replace(' ', '').replace('_', ''):
                additional_entry = AdditionalEntry()
                additional_entry.remove_from_rule(
                    self.get_target_model_cls(),
                    self.get_visit_model_instance(),
                    self.get_target_content_type_map())
