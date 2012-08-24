from datetime import datetime
from bhp_entry.models import Entry
from bhp_visit_tracking.classes import VisitModelHelper
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_entry.models import ScheduledEntryBucket
from base_entry import BaseEntry


class ScheduledEntry(BaseEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = ScheduledEntryBucket

    def get_user_model_base_cls(self):
        return BaseVisitTracking

    def get_visit_model_instance(self):
        return self.get_filter_model_instance()

    def set_filter_model_instance(self, filter_model_instance=None):
        """Sets the filter model instance to be a visit model instance."""
        if filter_model_instance:
            if not isinstance(filter_model_instance, self.get_user_model_base_cls()):
                AttributeError('Attribute _visit_model_instance must be an instance of BaseVisitTracking.')
            self._filter_model_instance = filter_model_instance

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreignkey that points to the visit model."""
        if self.get_user_model_cls() and self.get_filter_model_instance():
            visit_model_helper = VisitModelHelper()
            fk_fieldname_to_visit_model = visit_model_helper.get_visit_field(model=self.get_user_model_cls(), visit_model=self.get_filter_model_instance())
            if not fk_fieldname_to_visit_model:
                raise AttributeError('Model {0} does not have a key to visit model {1}.'.format(self.get_user_model_cls(), self.get_filter_model_instance()))
            self._filter_fieldname = fk_fieldname_to_visit_model

    def add_or_update_for_visit(self, visit_model_instance):
        """ Loops thru the list of entries configured for the visit_definition of this visit_model_instance
        and Adds entries to or updates existing entries in the bucket.

        This just determines KEYED or NEW, bucket rules with reassess later.
        """
        self.set_filter_model_instance(visit_model_instance)
        visit_model_instance = self.get_filter_model_instance()
        registered_subject = visit_model_instance.appointment.registered_subject
        # scheduled entries are only added if visit instance is 0
        if visit_model_instance.appointment.visit_instance == '0':
            filled_datetime = datetime.today()
            # fetch entries required for this the visit definition of this visit_model_instance.appointment
            for entry in Entry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition):
                self.set_user_model_cls_with_entry(entry)
                # TODO: calculate due date -- "needs work"
                report_datetime = visit_model_instance.report_datetime
                due_datetime = entry.visit_definition.get_upper_window_datetime(report_datetime)
                entry_status = self.get_status('NEW')
                if entry_status == 'NEW':
                    report_datetime = None
                options = {'current_entry_title': self.get_user_model_cls()._meta.verbose_name,
                           'fill_datetime': filled_datetime,
                           'due_datetime': due_datetime,
                           'report_datetime': report_datetime,
                           'entry_status': entry_status}
                bucket_instance, created = self.get_bucket_model_cls().objects.get_or_create(
                        registered_subject=registered_subject,
                        appointment=visit_model_instance.appointment,
                        entry=entry,
                        defaults=options)
                if not created:
                    bucket_instance.report_datetime = report_datetime
                    #if self.get_status(bucket_instance.entry_status) == 'KEYED':
                    bucket_instance.entry_status = entry_status
                    bucket_instance.save()
                    #print 'add or update  {0}'.format(datetime.today())

    def update_status(self, action, scheduled_entry_bucket_id, report_datetime, comment=None):
        """Updates status for a given scheduled_entry_bucket instance.

        Usually called from bucket controller."""
        bucket_instance = self.get_bucket_model_cls().objects.get(pk=scheduled_entry_bucket_id)
        #was = bucket_instance.entry_status
        bucket_instance.report_datetime = report_datetime
        status = self.get_status(action)
        bucket_instance.entry_status = status
        #print '{0} and is now {1}'.format(was, status)
        if comment:
            bucket_instance.comment = comment
        bucket_instance.save()
        #print 'update_status() {0}'.format(datetime.today())
