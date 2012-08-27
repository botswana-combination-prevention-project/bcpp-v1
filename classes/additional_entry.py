from bhp_entry.models import AdditionalEntryBucket
from base_entry import BaseEntry


class AdditionalEntry(BaseEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = AdditionalEntryBucket

    def add_from_rule(self, rule_name, visit_model_instance, content_type_map):
        """Add an entry to the bucket"""
        #print scheduled_entry_bucket_id
        options = {'due_datetime': visit_model_instance.report_datetime,
                   'rule_name': rule_name}
        self.get_bucket_model_cls().objects.get_or_create(
            registered_subject=visit_model_instance.appointment.registered_subject,
            content_type_map=content_type_map,
            defaults=options)
        #if not created:
        #    bucket_instance.due_datetime = visit_model_instance.report_datetime
        #    bucket_instance.save()

    def remove_from_rule(self, rule_name, target_model_cls, visit_model_instance, content_type_map):
        """Remove an entry to the bucket using criteria including the rule group.name.

        To avoid rules overriding eachother, only the rule that created the bucket_instance
        may delete the bucket_instance."""
        self.set_visit_model_instance(visit_model_instance)
        self.set_content_type_map(content_type_map)
        if not target_model_cls.objects.filter(registered_subject=self.get_visit_model_instance().appointment.registered_subject).exists():
            self.get_bucket_model_cls().objects.filter(
                rule_name=rule_name,
                registered_subject=self.get_visit_model_instance().appointment.registered_subject,
                content_type_map=self.get_content_type_map()).delete()
