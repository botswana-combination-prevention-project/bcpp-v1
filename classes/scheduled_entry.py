import copy
from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from bhp_entry.models import Entry
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_entry.models import ScheduledEntryBucket
from base_scheduled_entry import BaseScheduledEntry


class ScheduledEntry(BaseScheduledEntry):

    # these reasons are required, may also get a list of reasons from model but
    # still must at least use these words
    required_visit_model_reasons = ['missed', 'death', 'lost', 'scheduled', 'unscheduled']

    def set_bucket_model_cls(self):
        self._bucket_model_cls = ScheduledEntryBucket

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

    def check_visit_model_reason_field(self, visit_model_instance):
        """Confirms visit model has a reason attribute and the choices tuple uses required values correctly.

        Called before visit model instance is set for this class.

        You can override the default list of required reasons by overriding the method 'get_visit_reason_choices'
        on the visit model."""

        if 'get_visit_reason_choices' in dir(visit_model_instance):
            required_reasons = [tpl[0].lower() for tpl in visit_model_instance.get_visit_reason_choices()]
            # check that required reasons use the required key words
            found = []
            for word in self.required_visit_model_reasons:
                for reason in required_reasons:
                    if word.lower() in reason.lower():
                        found.append(word)
                        break
            if found != self.required_visit_model_reasons:
                raise ImproperlyConfigured('Visit model method \'get_visit_reason_choices\' must return a list of choices using each of the required words {0}. Got {1}.'.format(self.required_visit_model_reasons, required_reasons))
        else:
            required_reasons = self.required_visit_model_reasons
        for f in visit_model_instance.__class__._meta.fields:
            if f.name == 'reason':
                field = f
                break
        if not field:
            raise ImproperlyConfigured('Visit model requires field \'reason\'.')
        for word in required_reasons:
            if word in visit_model_instance.reason.lower() and visit_model_instance.reason.lower() != word:
                raise ImproperlyConfigured('Visit model attribute \'reason\' value \'{1}\' is invalid. Must be \'{0}\'. The words {2} are reserved, as is, for the reason choices tuple. Check your visit model\'s field or form field definition.'.format(word, visit_model_instance.reason.lower(), required_reasons))

    def add_or_update_for_visit(self, visit_model_instance):
        """ Loops thru the list of entries configured for the visit_definition of this visit_model_instance
        and Adds entries to or updates existing entries in the bucket.

        If reason for visit (visit tracking form) is not scheduled, deletes and/or does not create NEW.

        This just determines KEYED or NEW, bucket rules will reassess later.
        """
        self.set_visit_model_instance(visit_model_instance)
        self.set_filter_model_instance(self.get_visit_model_instance())
        registered_subject = visit_model_instance.appointment.registered_subject
        if 'get_visit_reason_choices' in dir(visit_model_instance):
            required_reasons = [tpl[0].lower() for tpl in visit_model_instance.get_visit_reason_choices()]
        else:
            required_reasons = self.required_visit_model_reasons
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
                if self.get_visit_model_instance().reason.lower() in required_reasons:
                    # is missed, lost or death, so delete NEW forms
                    self.get_bucket_model_cls().objects.filter(
                            registered_subject=registered_subject,
                            appointment=self.get_visit_model_instance().appointment,
                            entry=entry,
                            entry_status='NEW'
                            ).delete()
                else:
                    # is a scheduled/unscheduled visit, so get_or_create forms for entry
                    bucket_instance, created = self.get_bucket_model_cls().objects.get_or_create(
                            registered_subject=registered_subject,
                            appointment=self.get_visit_model_instance().appointment,
                            entry=entry,
                            defaults=options)
                    if not created and bucket_instance.entry_status != entry_status:
                        bucket_instance.report_datetime = report_datetime
                        bucket_instance.entry_status = entry_status
                        bucket_instance.save()

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
