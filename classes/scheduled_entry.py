from datetime import datetime, date
from django.db.models import get_model
from bhp_entry.models import Entry
from bhp_registration.models import RegisteredSubject
from bhp_visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from base_scheduled_entry import BaseScheduledEntry


class ScheduledEntry(BaseScheduledEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = get_model('bhp_entry', 'ScheduledEntryBucket')
        if not self._bucket_model_cls:
            raise TypeError('Unable to get model bhp_entry.ScheduledEntryBucket.')

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreignkey that points to the visit model."""
        self._filter_fieldname = None
        if filter_field_name:
            self._filter_fieldname = filter_field_name
        else:
            if self.get_target_model_instance():
                # look for a field value that is a base of BaseVisitTracking, the target_model_base_cls
                for field in self.get_target_model_cls()._meta.fields:
                    if field.rel:
                        if issubclass(field.rel.to, self.get_target_model_base_cls()):
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

#     def check_visit_model_reason_field(self, visit_model_instance):
#         """Confirms visit model has a reason attribute and the choices tuple uses required values correctly.
# 
#         Called before visit model instance is set for this class.
# 
#         You can override the default list of required reasons by overriding the method 'get_visit_reason_choices'
#         on the visit model."""
# 
#         #visit_reason_choices = visit_model_instance.get_visit_reason_choices()
#         visit_reason_choices = visit_model_instance._get_visit_reason_choices()
#         if not isinstance(visit_reason_choices, dict):
#             raise TypeError('Expected dictionary from get_visit_reason_choices(). Got {0}'.format(visit_reason_choices))
#         # check that the user visit reasons conform to use the required key words
#         found = []
#         visit_reason_required_keys = VISIT_REASON_REQUIRED_CHOICES
#         visit_reason_required_keys.sort()
#         for k in visit_reason_required_keys:
#             # look for each required word
#             for v in visit_reason_choices:
#                 if k == v:
#                     found.append(k)
#         found.sort()
#         if found != visit_reason_required_keys:
#             raise ImproperlyConfigured('Visit model method \'get_visit_reason_choices\' must return a list of choices using each of the required words {0}. Got {1}.'.format(visit_reason_required_keys, visit_reason_choices))
#         # ensure visir model has field reason
#         for f in visit_model_instance.__class__._meta.fields:
#             if f.name == 'reason':
#                 field = f
#                 break
#         if not field:
#             raise ImproperlyConfigured('Visit model requires field \'reason\'.')
#         #for word in required_reasons:
#         #    if word in visit_model_instance.reason.lower() and visit_model_instance.reason.lower() != word:
#         #        raise ImproperlyConfigured('Visit model attribute \'reason\' value \'{1}\' is invalid. Must be \'{0}\'. The words {2} are reserved, as is, for the reason choices tuple. Check your visit model\'s field or form field definition.'.format(word, visit_model_instance.reason.lower(), required_reasons))
#         return visit_reason_choices

    def show_scheduled_entries(self, registered_subject, visit_model_instance=None):
        visit_model_instance = visit_model_instance or self.get_visit_model_instance()
        if 'get_visit_reason_no_follow_up_choices' in dir(visit_model_instance):
            visit_reason_no_follow_up_choices = visit_model_instance.get_visit_reason_no_follow_up_choices()
        else:
            visit_reason_no_follow_up_choices = VISIT_REASON_NO_FOLLOW_UP_CHOICES
        show_scheduled_entries = visit_model_instance.reason.lower() not in [x.lower() for x in visit_reason_no_follow_up_choices.itervalues()]
        # possible conditions that override above
        # subject is at the off study visit (lost)
        if visit_model_instance.reason.lower() in visit_model_instance.get_off_study_reason():
            visit_date = date(visit_model_instance.report_datetime.year, visit_model_instance.report_datetime.month, visit_model_instance.report_datetime.day)
            if visit_model_instance.get_off_study_cls().objects.filter(registered_subject=registered_subject, offstudy_date=visit_date):
                # has an off study form completed on same day as visit
                off_study_instance = visit_model_instance.get_off_study_cls().objects.get(registered_subject=registered_subject, offstudy_date=visit_date)
                show_scheduled_entries = off_study_instance.show_scheduled_entries_on_off_study_date()
        return show_scheduled_entries

    def add_or_update_for_visit(self, visit_model_instance):
        """ Loops thru the list of entries configured for the visit_definition of this visit_model_instance
        and Adds entries to or updates existing entries in the bucket.

        If reason for visit (visit tracking form) is not scheduled, deletes and/or does not create NEW.

        This just determines KEYED or NEW, bucket rules will reassess later.
        """
        self.set_visit_model_instance(visit_model_instance)
        self.set_filter_model_instance(self.get_visit_model_instance())
        registered_subject = visit_model_instance.appointment.registered_subject
        show_scheduled_entries = self.show_scheduled_entries(registered_subject)
        #visit_reason_choices = visit_model_instance._get_visit_reason_choices()

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
                if not show_scheduled_entries:
                    # is missed, lost or death, so delete NEW forms
                    self.get_bucket_model_cls().objects.filter(
                            registered_subject=registered_subject,
                            appointment=self.get_visit_model_instance().appointment,
                            entry=entry,
                            entry_status__in=['NEW', 'NOT_REQUIRED'],
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

    def get_next_entry_for(self, entry_order, appointment, registered_subject):
        next_bucket_instance = None
        options = {
           'registered_subject_id': registered_subject.pk,
           'appointment_id': appointment.pk,
           #'entry__entry_category': entry_category,
            'entry_status': 'NEW',
            'entry__entry_order__gt': entry_order}
        if self.get_bucket_model_cls().objects.filter(**options):
            next_bucket_instance = self.get_bucket_model_cls().objects.filter(**options)[0]
        return next_bucket_instance

    def get_entries_for(self, appointment, entry_category, registered_subject=None, entry_status=None):
        """Returns a list of Bucket instance for the given subject and zero instance appointment."""
        if str(appointment.visit_instance) != str('0'):
            raise TypeError('Appointment must be a 0 instance appointment.')
        if not registered_subject:
            registered_subject = appointment.registered_subject
        if not isinstance(registered_subject, RegisteredSubject):
            raise TypeError('Expected an instance of RegisteredSubject.')
        bucket_instances = []
        if appointment:
            options = {
               'registered_subject_id': registered_subject.pk,
               'appointment_id': appointment.pk,
               'entry__entry_category': entry_category,
               }
            if entry_status:
                options.update({'entry_status': entry_status})
            bucket_instances = self.get_bucket_model_cls().objects.filter(**options).order_by('entry__entry_order')
        return bucket_instances
