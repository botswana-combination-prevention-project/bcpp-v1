from datetime import datetime
from bhp_entry.models import Entry
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_entry.models import ScheduledEntryBucket
from base_entry import BaseEntry


class ScheduledEntry(BaseEntry):
    def set_bucket_model_cls(self):
        self._bucket_model_cls = ScheduledEntryBucket

    def set_target_model_base_cls(self):
        self._target_model_base_cls = BaseVisitTracking

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreignkey that points to the visit model."""
        self._filter_fieldname = None
        if filter_field_name:
            self._filter_fieldname = filter_field_name
        else:
            if self.get_target_model_instance():
                # look for a field value that is a base of BaseVisitTracking
                for field in self.get_target_model_cls()._meta.fields:
                    if field.rel:
                        if issubclass(field.rel.to, BaseVisitTracking):
                            self._filter_fieldname = field.name
                            break
            else:
                pass

    def set_bucket_model_instance(self, bucket_model_instance=None):
        if bucket_model_instance:
            if not isinstance(bucket_model_instance, self.get_bucket_model_cls()):
                raise AttributeError('Attribute _bucket_model_instance must be an instance of {0}. Got {1}'.format(self.get_bucket_model_cls(), bucket_model_instance.__class__))
        if not bucket_model_instance:
            # try to get by searching bucket model
            try:
                entry = Entry.objects.get(
                    visit_definition=self.get_visit_model_instance().appointment.visit_definition,
                    content_type_map=self.content_type_map)
            except:
                raise
            try:
                bucket_model_instance = self.get_bucket_model_cls().objects.get(
                    appointment=self.get_visit_model_instance().appointment,
                    registered_subject=self.get_visit_model_instance().appointment.registered_subject,
                    entry=entry)
            except:
                pass
        self._bucket_model_instance = bucket_model_instance

    def add_or_update_for_visit(self, visit_model_instance):
        """ Loops thru the list of entries configured for the visit_definition of this visit_model_instance
        and Adds entries to or updates existing entries in the bucket.

        This just determines KEYED or NEW, bucket rules with reassess later.
        """
        self.set_visit_model_instance(visit_model_instance)
        self.set_filter_model_instance(self.get_visit_model_instance())
        registered_subject = visit_model_instance.appointment.registered_subject
        # scheduled entries are only added if visit instance is 0
        if self.get_visit_model_instance().appointment.visit_instance == '0':
            filled_datetime = datetime.today()
            # fetch entries required for this the visit definition of this visit_model_instance.appointment
            for entry in Entry.objects.filter(visit_definition=self.get_visit_model_instance().appointment.visit_definition):
                self.set_target_model_cls_with_entry(entry)
                # TODO: calculate due date -- "needs work"
                report_datetime = self.get_visit_model_instance().report_datetime
                due_datetime = entry.visit_definition.get_upper_window_datetime(report_datetime)
                entry_status = self.get_status('NEW')
                if entry_status == 'NEW':
                    report_datetime = None
                options = {'current_entry_title': self.get_target_model_cls()._meta.verbose_name,
                           'fill_datetime': filled_datetime,
                           'due_datetime': due_datetime,
                           'report_datetime': report_datetime,
                           'entry_status': entry_status}
                bucket_instance, created = self.get_bucket_model_cls().objects.get_or_create(
                        registered_subject=registered_subject,
                        appointment=self.get_visit_model_instance().appointment,
                        entry=entry,
                        defaults=options)
                if not created and bucket_instance.entry_status != entry_status:
                    bucket_instance.report_datetime = report_datetime
                    bucket_instance.entry_status = entry_status
                    bucket_instance.save()

    def update_bucket(self, action, report_datetime=None, comment=None):
        bucket_instance = self.get_bucket_model_instance()
        if not bucket_instance:
            raise TypeError('Attribute for bucket model instance cannot be None.')
        if not report_datetime:
            self.get_filter_model_instance().report_datetime
        bucket_instance.report_datetime = report_datetime
        if comment:
            bucket_instance.entry_comment = comment
        else:
            bucket_instance.entry_comment = ''
        entry_status = self.get_status(action)
        bucket_instance.entry_status = entry_status
        #if entry_status.lower() != action.lower():
        bucket_instance.save()
        #print 'updated from {0} to {1}.for {2}'.format(action, entry_status, bucket_instance)

    def update_status_from_instance(self, action, target_model_instance, filter_model_cls, comment=None):
        "Sets up then calls update bucket using a user model instance."""
        self.set_target_model_cls(target_model_instance.__class__)
        self.set_target_model_instance(target_model_instance)
        self.set_target_model_cls(filter_model_cls)
        self.update_bucket(action, None, comment)

    def update_status_from_rule(self, action, target_model_cls, scheduled_entry_bucket_id, visit_model_instance, filter_model_instance, filter_model_field, comment=None):
        """Sets up then calls update bucket given a bucket instance id.

        Usually called from bucket controller."""
        #print scheduled_entry_bucket_id
        self.reset(visit_model_instance)
        self.set_target_model_cls(target_model_cls)
        self.set_filter_model_instance(filter_model_instance)
        self.set_filter_fieldname(filter_model_field)
        self.set_bucket_model_instance_with_id(scheduled_entry_bucket_id)
        self.update_bucket(action, visit_model_instance.report_datetime, comment)

    def get_entries_for(self, appointment, entry_category):
        """Returns a list of Bucket instance for the given subject and zero instance appointment."""
        if appointment.visit_instance != '0':
            raise TypeError('Appointment must be a 0 instance appointment.')
        registered_subject_id = appointment.registered_subject.pk
        bucket_instance_list = []
        if appointment:
            for  bucket_instance in self.get_bucket_model_cls().objects.values('pk').filter(
                registered_subject_id=registered_subject_id,
                appointment_id=appointment.pk,
                entry__entry_category=entry_category,
                ).order_by('entry__entry_order'):
                bucket_instance_list.append(self.get_bucket_model_cls().objects.select_related().get(pk=bucket_instance.get('pk')))
        return bucket_instance_list