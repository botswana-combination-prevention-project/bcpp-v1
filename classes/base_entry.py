from datetime import datetime
from django.core.exceptions import FieldError, ImproperlyConfigured
from bhp_entry.models import Entry
from bhp_entry.models import BaseEntryBucket


class BaseEntry(object):

    def __init__(self):
        self._filter_fieldname = None
        self._filter_model_instance = None
        self._user_model_cls = None
        self._bucket_model_cls = None
        self._bucket_model_instance = None
        self._user_model_instance = None
        self.user_model_base_cls = None

    def get_user_model_base_cls(self):
        return object

    def set_filter_fieldname(self, filter_field_name=None):
        """ Returns the field name to be used to \'get\'  the model_instance or filter the model class.

        Users need to override this

        For example may return \'registered_subject\' for bucket model classes that do
        not have a visit model foreign key.
        """
        if self._filter_fieldname is None:
            raise TypeError('Attribute filter_fieldname cannot be None. Override this method in the subclass.')

    def get_filter_fieldname(self):
        if not self._filter_fieldname:
            self.set_filter_fieldname()
        return self._filter_fieldname

    def set_filter_model_instance(self, filter_model_instance=None):
        """Sets the filter model instance to be a visit model instance."""
        if filter_model_instance:
            if not isinstance(filter_model_instance, self.get_user_model_base_cls()):
                AttributeError('Attribute _filter_model_instance must be an instance of {0}.'.format(self.get_user_model_base_cls()))
            self._filter_model_instance = filter_model_instance

#    def set_filter_model_instance(self):
#        """Sets a model instance that will be used with the filter_field name as the criteria to filter or get the model that we are tracking.
#
#        Users should override this to return a model instance that matches the filter filed name."""
#        if self._filter_model_instance is None:
#            raise TypeError('Attribute _filter_model_instance cannot be None. Override this method in the subclass.')

    def get_filter_model_instance(self):
        if not self._filter_model_instance:
            self.set_filter_model_instance()
        return self._filter_model_instance

    def set_user_model_cls_with_entry(self, entry_model_instance):
        self.set_user_model_cls(entry_model_instance.content_type_map.model_class())

    def set_user_model_cls(self, model_cls=None):
        """Sets the user's model class that the entry class is tracking."""
        if model_cls is None:
            raise AttributeError('Attribute entry_model_instance cannot be None.')
        if not issubclass(model_cls, self.get_user_model_base_cls()):
            AttributeError('Attribute _entry_model_instanc must be an instance of {0}.'.format(self.get_user_model_base_cls()))
        self._user_model_cls = model_cls
        # if the class has changed the instance must be updated
        self._user_model_instance = None

    def get_user_model_cls(self):
        if not self._user_model_cls:
            self.set_user_model_cls()
        return self._user_model_cls

    def set_user_model_instance(self, user_model_instance=None):
        """ Returns the instance of the user's model class being tracked if it can."""
        self._user_model_instance = None
        if user_model_instance:
            self._user_model_instance = user_model_instance
            self.set_user_model_cls(self._user_model_instance.__class__)
        elif self.get_filter_fieldname() and self.get_filter_model_instance():
            if self.get_user_model_cls().objects.filter(**{self.get_filter_fieldname(): self.get_filter_model_instance()}).exists():
                self._user_model_instance = self.get_user_model_cls().objects.get(**{self.get_filter_fieldname(): self.get_filter_model_instance()})

    def get_user_model_instance(self):
        if not self._user_model_instance:
            self.set_user_model_instance()
        return self._user_model_instance

#    def set_entry_model_instance(self, entry_model_instance=None):
#        if not entry_model_instance:
#            raise AttributeError('Attribute _entry_model_instanc cannot be None.')
#        if not isinstance(entry_model_instance, Entry):
#            AttributeError('Attribute _entry_model_instanc must be an instance of Entry.')
#        self._entry_model_instanc = entry_model_instance
#
#    def get_entry_model_instance(self):
#        if not self._entry_model_instance:
#            self.set_entry_model_instance()
#        return self._entry_model_instance

    def set_bucket_model_instance(self, bucket_model_instance=None):
        if not bucket_model_instance:
            raise AttributeError('Attribute _bucket_model_instance cannot be None.')
        if not isinstance(bucket_model_instance, BaseEntryBucket):
            raise AttributeError('Attribute _entry must be an instance of BaseEntryBucket.')
        self._bucket_model_instance = bucket_model_instance

    def get_bucket_model_instance(self):
        if not self._bucket_model_instance:
            self.set_bucket_model_instance()
        return self._bucket_model_instance

    def set_bucket_model_cls(self):
        if self._bucket_model_cls is None:
            raise AttributeError('Attribute _bucket_model_cls cannot be None.')

    def get_bucket_model_cls(self):
        if not self._bucket_model_cls:
            self.set_bucket_model_cls()
        return self._bucket_model_cls

    def is_keyed(self):
        """ Indicates that the model instance exists (and is therefore keyed).  """
        if self.get_user_model_instance():
            return True
        else:
            return False

    def get_status(self, action):
        """Figures out the the current status of the user model instance, KEYED or NEW (not keyed)."""
        action = action.upper()
        action_terms = ['NEW', 'KEYED', 'NOT_REQUIRED', 'DELETE']
        if action not in action_terms:
            raise ValueError('Action must be %s. Got %s' % (action_terms, action))
        if self.is_keyed():
            retval = 'KEYED'
        else:
            retval = action
        if action == 'DELETE':
            retval = 'NEW'
        return retval

    def get_entries_for(self, appointment, entry_category):
        """Returns a list of ScheduledEntryBucket instance for the given subject and zero instance appointment."""
        if appointment.visit_instance != '0':
            raise TypeError('Appointment must be a 0 instance appointment.')
        registered_subject_id = appointment.registered_subject.pk
        bucket_instance_list = []
        if appointment:
            for  bucket_instance in self.get_bucket_model_cls().objects.values('pk').filter(registered_subject_id=registered_subject_id,
                                                                                    appointment_id=appointment.pk,
                                                                                    entry__entry_category=entry_category,
                                                                                    ).order_by('entry__entry_order'):
                bucket_instance_list.append(self.get_bucket_model_cls().objects.select_related().get(pk=bucket_instance.get('pk')))
        return bucket_instance_list

#    def update_status(self, model, visit_model_instance, action, comment=None):
#
#        """Updates bucket status, etc for a given entry in bucket.
#        usually called from bucket controller.
#        """
#        action_terms = ['new', 'keyed', 'not_required', 'delete']
#        if action not in action_terms:
#            raise ValueError('Action must be %s. Got %s' % (action_terms, action))
#        # try to update
#        # if self.entry is None implies Entry has no occurrence for this visit_definition, content_type_map,
#        # which is OK.
#        # see method set_entry()
#        if Entry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition).exists():
#            entry = Entry.objects.get(visit_definition=visit_model_instance.appointment.visit_definition)
#            if visit_model_instance:
#                if super(ScheduledEntryBucketManager, self).filter(registered_subject=self.registered_subject,
#                                                                   appointment=self.appointment,
#                                                                   entry=entry).exists():
#                    # already in bucket, so get bucket entry
#                    bucket_instance = super(ScheduledEntryBucketManager, self).get(registered_subject=self.registered_subject,
#                                                                                          appointment=self.appointment,
#                                                                                          entry=entry)
#                    # update entry_status if NEW no matter what, to indictate perhaps that it was modified
#                    status = self.get_status(
#                        action=action,
#                        report_datetime=self.report_datetime,
#                        current_status=bucket_instance.entry_status,
#                        entry_comment=comment)
#                    bucket_instance.report_datetime = status['report_datetime']
#                    bucket_instance.entry_status = status['action']
#                    bucket_instance.entry_comment = status['entry_comment']
#                    bucket_instance.close_datetime = status['close_datetime']
#                    bucket_instance.modified = datetime.today()
#                    bucket_instance.save()
#                else:
#                    # create a new scheduled bucket entry instance
#                    #
#                    super(ScheduledEntryBucketManager, self).create(
#                        created=datetime.today(),
#                        modified=datetime.today(),
#                        registered_subject=self.registered_subject,
#                        current_entry_title=entry.content_type_map.model.lower(),
#                        entry_status='NEW',
#                        due_datetime=None,
#                        report_datetime=datetime.today(),
#                        entry_comment='auto',
#                        close_datetime=None,
#                        fill_datetime=None,
#                        appointment=self.appointment,
#                        entry=entry)
#            else:
#                raise AttributeError('Cannot determine visit model. See %s update_status()' % (self,))
