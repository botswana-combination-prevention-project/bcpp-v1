from bhp_entry.models import BaseEntryBucket
from bhp_content_type_map.models import ContentTypeMap


class BaseEntry(object):
    """ Base class for all classes that manage the entry state of additional, scheduled and unscheduled data."""
    def __init__(self):
        self._filter_fieldname = None  # field to filter the target_model
        self._filter_model_instance = None  # instance of field to filter the user model
        self._target_model_cls = None
        self._bucket_model_cls = None  # for example, ScheduledEntryBucket, AdditionalEnrtyBucket
        self._bucket_model_instance = None
        self._target_model_base_cls = None  # for error reporting
        self._content_type_map = None  # to help get the correct instance from the model 'Entry'
        self._target_model_instance = None
        self._visit_model_instance = None
        self._visit_model_fieldname = None
        self._visit_model_base_cls = None

    def reset(self, visit_model_instance):
        self._bucket_model_instance = None
        self._target_model_instance = None
        self._filter_model_instance = None
        self._visit_model_instance = None
        self.set_visit_model_instance(visit_model_instance)

    def set_visit_model_base_cls(self):
        from bhp_visit_tracking.models import BaseVisitTracking
        self._visit_model_base_cls = BaseVisitTracking

    def get_visit_model_base_cls(self):
        if not self._visit_model_base_cls:
            self.set_visit_model_base_cls()
        return self._visit_model_base_cls

    def set_visit_model_instance(self, visit_model_instance=None):
        if not isinstance(visit_model_instance, self.get_visit_model_base_cls()):
            raise TypeError('Parameter \'visit_model_instance\' must be an instance of BaseVisitTracking. Got {0}'.format(visit_model_instance))
        self.check_visit_model_reason_field(visit_model_instance)
        self._visit_model_instance = visit_model_instance
        if not self._visit_model_instance:
            raise AttributeError('Attribute _visit_model_instance cannot be None')

    def check_visit_model_reason_field(self, visit_model_instance):
        """Confirms visit model has a reason attribute and the choices tuple uses required values correctly."""
        pass

    def get_visit_model_instance(self):
        if not self._visit_model_instance:
            self.set_visit_model_instance()
        return self._visit_model_instance

    def set_filter_fieldname(self, filter_field_name=None):
        """ Returns the field name to be used to \'get\'  the target_model_instance or filter the user model class.

        Users need to override this

        For example may return \'registered_subject\' for bucket model classes that do
        not have a visit model foreign key.
        """
        if self._filter_fieldname is None:
            raise TypeError('Attribute filter_fieldname cannot be None. Override this method in the subclass.')

    def set_visit_model_fieldname(self, visit_model_fieldname=None):
        """Returns the field name for the foreignkey that points to the visit model."""
        self._visit_model_fieldname = None
        if visit_model_fieldname:
            self._visit_model_fieldname = visit_model_fieldname
        else:
            if self.get_target_model_cls():
                # look for a field value that is a base of
                for field in self.get_target_model_cls()._meta.fields:
                    if field.rel:
                        if issubclass(field.rel.to, self.get_visit_model_base_cls()):
                            self._visit_model_fieldname = field.name
                            break
            else:
                pass
        if not self._visit_model_fieldname:
            raise AttributeError('Attribute _visit_model_fieldname cannot be None. Check the models listed in your visit definition.')

    def get_visit_model_fieldname(self):
        if not self._visit_model_fieldname:
            self.set_visit_model_fieldname()
        return self._visit_model_fieldname

    def set_target_model_base_cls(self):
        """Users need to override this to set to something like BaseVisitTracking."""
        if self._target_model_base_cls is None:
            raise AttributeError('Attribute _target_model_base_cls cannot be None.')

    def get_target_model_base_cls(self):
        if not self._target_model_base_cls:
            self.set_target_model_base_cls()
        return self._target_model_base_cls

    def set_filter_model_instance(self, filter_model_instance=None):
        """Sets the filter model instance to be the users visit model instance."""
        if filter_model_instance:
            if not isinstance(filter_model_instance, self.get_target_model_base_cls()):
                AttributeError('Attribute _filter_model_instance must be an instance of {0}.'.format(self.get_target_model_base_cls()))
            self._filter_model_instance = filter_model_instance

    def get_filter_fieldname(self):
        if not self._filter_fieldname:
            self.set_filter_fieldname()
        return self._filter_fieldname

    def get_filter_model_instance(self):
        if not self._filter_model_instance:
            self.set_filter_model_instance()
        return self._filter_model_instance

    def set_target_model_cls_with_entry(self, entry_model_instance):
        self.set_target_model_cls(entry_model_instance.content_type_map.model_class())

    def set_target_model_cls(self, model_cls=None):
        """Sets the user's model class that the entry class is tracking."""
        if model_cls is None:
            raise AttributeError('Attribute model_cls cannot be None.')
        if not issubclass(model_cls, self.get_target_model_base_cls()):
            AttributeError('Attribute model_cls must be an instance of {0}.'.format(self.get_target_model_base_cls()))
        self._target_model_cls = model_cls
        # if the class must match the instance, if not null the instance
        if self._target_model_instance:
            if not isinstance(self._target_model_instance, self._target_model_cls):
                self._target_model_instance = None

    def get_target_model_cls(self):
        if not self._target_model_cls:
            self.set_target_model_cls()
        return self._target_model_cls

    def set_target_model_instance(self, target_model_instance=None):
        raise TypeError("Method must be overridden")

    def get_target_model_instance(self):
        if not self._target_model_instance:
            self.set_target_model_instance()
        return self._target_model_instance

    def set_bucket_model_instance(self, bucket_model_instance=None):
        if bucket_model_instance:
            if not isinstance(bucket_model_instance, BaseEntryBucket):
                raise AttributeError('Attribute _bucket_model_instance must be an instance of BaseEntryBucket. Got {0}'.format(bucket_model_instance))
        self._bucket_model_instance = bucket_model_instance

    def set_bucket_model_instance_with_id(self, bucket_model_instance_id):
        self.set_bucket_model_instance(self.get_bucket_model_cls().objects.get(pk=bucket_model_instance_id))

    def get_bucket_model_instance(self):
        if not self._bucket_model_instance:
            self.set_bucket_model_instance()
        return self._bucket_model_instance

    def set_bucket_model_cls(self):
        """Users need to override this to set with something like ScheduledEnrtyBucket."""
        if self._bucket_model_cls is None:
            raise AttributeError('Attribute _bucket_model_cls cannot be None.')

    def get_bucket_model_cls(self):
        if not self._bucket_model_cls:
            self.set_bucket_model_cls()
        return self._bucket_model_cls

    def set_content_type_map(self, content_type_map=None):
        if content_type_map:
            self._content_type_map = content_type_map
        else:
            model = self.get_target_model_cls() or self.get_target_model_instance()
            if model:
                self._content_type_map = ContentTypeMap.objects.get(
                    app_label=self.model._meta.app_label,
                    name=self.model._meta.verbose_name)
            else:
                self._content_type_map = None

    def get_content_type_map(self):
        if not self._content_type_map:
            self.set_content_type_map()
        return self._content_type_map

    def is_keyed(self):
        """ Indicates that the model instance exists (and is therefore keyed).  """
        if self.get_target_model_instance():
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
        bucket_instance.save()
