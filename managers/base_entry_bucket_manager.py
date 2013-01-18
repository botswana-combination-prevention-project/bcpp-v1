from django.db import models
from django.db.models import get_model


class BaseEntryBucketManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.visit_model_instance = None
        self.visit_definition = None
        self.report_datetime = None
        self.appointment = None
        self.entry = None
        super(BaseEntryBucketManager, self).__init__(*args, **kwargs)

    def set_entry(self):
        """Finds occurrence for this visit_definition in the Entry model and if not found, update_status() has nothing to do."""
        model = get_model('bhp_entry', 'Entry')
        if model.objects.filter(visit_definition=self.visit_definition, content_type_map=self.content_type_map):
            self.entry = model.objects.get(visit_definition=self.visit_definition, content_type_map=self.content_type_map)
        else:
            self.entry = None

    def set_appointment(self):
        self.appointment = self.visit_model_instance.appointment.__class__.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code=self.visit_model_instance.appointment.visit_definition.code,
                visit_instance='0')

    def is_keyed(self):
        """ Confirm if model instance exists / is_keyed """
        raise AttributeError('is_keyed() may not be called on the base model %' % (self,))

    def get_status(self, **kwargs):
        """Returns the status of the entry bucket instance.

        Options are:

            * NEW
            * KEYED
            * NOT REQUIRED

        """
        desired_action = kwargs.get("action")
        report_datetime = kwargs.get("report_datetime")
        entry_comment = kwargs.get("comment")
        # get the current status of the record, KEYED or NEW (not keyed)
        if self.is_keyed():
            current_status = 'KEYED'
        else:
            current_status = 'NEW'
        if current_status == 'KEYED' and not desired_action == 'delete':
            # keep return action as keyed if the record is KEYED. regardless
            # of the desired action
            report_datetime = report_datetime
            if desired_action == 'not_required':
                entry_comment = 'NOT REQUIRED!'
            return_action = 'KEYED'
        else:
            if desired_action == 'add_change':
                report_datetime = report_datetime
                return_action = 'KEYED'
                entry_comment = ''
            elif desired_action == 'delete':
                report_datetime = None
                return_action = 'NEW'
                entry_comment = 'deleted'
            elif desired_action == 'new':
                report_datetime = None
                return_action = 'NEW'
                entry_comment = 'required'
            elif desired_action == 'not_required':
                report_datetime = None
                return_action = 'NOT_REQUIRED'
                entry_comment = ''
            else:
                raise ValueError('In update_status, value of \'action\' is unhandled. Got %s.' % desired_action)
        close_datetime = None
        return {'action': return_action.upper(),
                'report_datetime': report_datetime,
                'entry_comment': entry_comment,
                'close_datetime': close_datetime}

    def _set_visit_model(self, **kwargs):
        """Gets visit_fk_name only if visit_model_instance is not provided."""
        self.visit_model = kwargs.get('visit_model')
        if not self.visit_model and not self.visit_model_instance:
            raise AttributeError('EntryBucketManager.update_status requires attribute \'visit_model\' if visit_model_instance is not provided. Got None')
