from bhp_entry.models import AdditionalEntryBucket
from base_entry import BaseEntry


class AdditionalEntry(BaseEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = AdditionalEntryBucket

    def add_from_rule(self, visit_model_instance, content_type_map):
        """Add an entry to the bucket"""
        #print scheduled_entry_bucket_id
        self.get_bucket_model_cls().objects.create(
            registered_subject=visit_model_instance.appointment.registered_subject,
            content_type_map=content_type_map)

    def remove_from_rule(self, target_model_cls, visit_model_instance, content_type_map):
        """Add an entry to the bucket"""
        if not target_model_cls.objects.filter(registered_subject=self.get_visit_model_instance().appointment.registered_subject).exists():
            self.get_bucket_model_cls().objects.filter(
                registered_subject=visit_model_instance.appointment.registered_subject,
                content_type_map=content_type_map).delete()
