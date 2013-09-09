from datetime import datetime
from django.core.exceptions import FieldError
from bhp_entry.models import AdditionalEntryBucket
from base_registered_subject_entry import BaseRegisteredSubjectEntry


class AdditionalEntry(BaseRegisteredSubjectEntry):

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

    def set_target_model_instance(self, target_model_instance=None):
        self._target_model_instance = None
        if target_model_instance:
            self._target_model_instance = target_model_instance
            self.set_target_model_cls(self._target_model_instance.__class__)
        elif self.get_registered_subject_instance():
            try:
                if self.get_target_model_cls().objects.filter(registered_subject=self.get_registered_subject_instance()).exists():
                    self._target_model_instance = self.get_target_model_cls().objects.get(registered_subject=self.get_registered_subject_instance())
            except FieldError as e:
                raise FieldError('Field \'registered_subject\' does not exist in model class {1}. Got {2}'.format(self.get_target_model_cls(), e))
            except:
                raise
        else:
            pass

    def update_for_registered_subject(self, registered_subject):
        """ Loops thru the list of entries configured for this registered subject
        and updates existing entries in the bucket.

        This just determines KEYED or NEW, bucket rules with reassess later.
        """
        # get the additioanl entries for this registered subject
        # check if the instance exists for any
        # update as keyed if exists
        # update as NEW if not exists
        self._set_registered_subject_instance(registered_subject)
        for bucket_model_instance in self.get_bucket_model_cls().objects.filter(registered_subject=registered_subject):
            self.set_bucket_model_instance(bucket_model_instance)
            self.set_target_model_cls_with_content_type()
            if not self.get_target_model_cls().objects.filter(registered_subject=self.get_registered_subject_instance()).exists():
                entry_status = 'NEW'
            else:
                self.set_target_model_instance()
                entry_status = self.get_status('NEW')
                try:
                    report_datetime = self.get_target_model_instance().get_report_datetime()
                except:
                    report_datetime = None
                filled_datetime = datetime.today()
            if entry_status == 'NEW':
                report_datetime = None
                filled_datetime = None
            if self.get_bucket_model_instance().entry_status != entry_status:
                self.get_bucket_model_instance().report_datetime = report_datetime
                self.get_bucket_model_instance().filled_datetime = filled_datetime
                self.get_bucket_model_instance().current_entry_title = self.get_target_model_cls()._meta.verbose_name
                self.get_bucket_model_instance().entry_status = entry_status
                self.get_bucket_model_instance().save()