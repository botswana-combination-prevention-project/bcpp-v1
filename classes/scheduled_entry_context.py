import copy
from django.db.models import get_model
from django.core.urlresolvers import reverse
from bhp_common.utils import convert_from_camel


class ScheduledEntryContext(object):

    """A Class used by the dashboard when rendering the list of scheduled entries to display under "Scheduled Forms"."""

    def __init__(self, scheduled_entry, appointment, visit_model):
        self._scheduled_entry = None
        self._model_pk = None
        self._app_label = None
        self._entry = None
        self._entry_status = None
        self._model_verbose_name = None
        self._model_inst = None
        self._appointment = appointment
        self._visit_model = visit_model
        self.set_scheduled_entry(scheduled_entry)
        self.set_model_inst()

    def get_context(self):
        """Returns a dictionary for the template context including all fields from ScheduledEntryBucket, URLs, etc.

        .. note:: The main purpose of this class is to return the template context."""
        context = copy.deepcopy(self.get_scheduled_entry().__dict__)
        del context['_entry_cache']
        del context['_state']
        context.update({
            'user_created': None,
            'user_modified': None,
            'created': None,
            'modified': None,
            'status': self.get_entry_status(),
            'model_pk': self.get_model_pk(),
            'entry': self.get_entry(),
            'label': self.get_model_verbose_name(),
            'entry_order': self.get_entry_order(),
            'group_title': self.get_group_title(),
            'model_url': self.get_model_url(),
            'scheduled_entry_url': self.get_scheduled_entry_url(),
            'databrowse_url': self.get_databrowse_url(),
            'audit_trail_url': self.get_audit_trail_url(),
            })
        if self.get_model_inst():
            context.update({
                'user_created': self.get_model_inst().user_created,
                'user_modified': self.get_model_inst().user_modified,
                'created': self.get_model_inst().created,
                'modified': self.get_model_inst().modified,
                })

        return context

    def set_scheduled_entry(self, value=None):
        """Sets to the schedule entry instance received on __init__."""
        self._scheduled_entry = value

    def get_scheduled_entry(self):
        if not self._scheduled_entry:
            self.set_scheduled_entry()
        return self._scheduled_entry

    def set_model_inst(self):
        """Sets to the model instance refered to by the scheduled entry."""
        self._model_inst = None
        options = {convert_from_camel(self.get_visit_model_instance()._meta.object_name): self.get_visit_model_instance()}
        if self.get_model_cls().objects.filter(**options):
            self._model_inst = self.get_model_cls().objects.get(**options)

    def get_model_inst(self):
        return self._model_inst

    def set_model_pk(self, value=None):
        """Sets to the pk of the model instance.

        .. seealso:: :func:`set_model_inst`"""

        self._model_pk = None
        if self.get_model_inst():
            self._model_pk = self.get_model_inst().pk

    def get_model_pk(self):
        if not self._model_pk:
            self.set_model_pk()
        return self._model_pk

    def set_entry(self):
        """Sets to the Entry instance related to the scheduled entry."""
        self._entry = self.get_scheduled_entry().entry

    def get_entry(self):
        if not self._entry:
            self.set_entry()
        return self._entry

    def get_visit_model(self):
        """Returns the visit model class."""
        return self._visit_model

    def get_visit_model_instance(self):
        """Returns and instance of the visit model taken from the appointment."""
        return getattr(self.get_appointment(), self.get_visit_model()._meta.object_name.lower())

    def get_model_verbose_name(self):
        """Returns the verbose name of the model referred to by the scheduled entry."""
        return self.get_model_cls()._meta.verbose_name

    def get_model_cls(self):
        """Returns the model class of the model referred to by the scheduled entry."""
        return get_model(self.get_app_label(), self.get_model_name())

    def get_app_label(self):
        return self.get_entry().content_type_map.app_label

    def get_model_name(self):
        return self.get_entry().content_type_map.model

    def get_appointment(self):
        """returns the current appointment."""
        return self._appointment

    def get_group_title(self):
        return self.get_entry().group_title

    def get_entry_order(self):
        return self.get_entry().entry_order

    def set_entry_status(self):
        self._entry_status = self.get_scheduled_entry().entry_status

    def get_entry_status(self):
        if not self._entry_status:
            self.set_entry_status()
        return self._entry_status

    def get_model_url(self):
        """Returns the URL to the model referred to by the scheduled entry."""
        model_url = None
        if self.get_appointment().appt_status == 'in_progress':
            if self.get_scheduled_entry().entry_status == 'NEW':
                model_url = reverse('admin:{app_label}_{model_name}_add'.format(app_label=self.get_app_label(), model_name=self.get_model_name()))
            elif self.get_scheduled_entry().entry_status == 'KEYED':
                if self.get_model_pk():
                    model_url = reverse('admin:{app_label}_{model_name}_change'.format(app_label=self.get_app_label(), model_name=self.get_model_name()), args=(self.get_model_pk(), ))
            else:
                pass  # could be NOT_REQUIRED
        return model_url

    def get_scheduled_entry_url(self):
        """Returns the URL for the scheduled entry."""
        if self.get_appointment().appt_status == 'in_progress':
            return reverse('admin:{app_label}_{model_name}_change'.format(app_label='bhp_entry', model_name='scheduledentrybucket'), args=(self.get_scheduled_entry().pk, ))
        return ''

    def get_databrowse_url(self):
        """Returns the URL to display this model instance using databrowse."""
        if self.get_model_inst():
            return '/databrowse/{app_label}/{model_name}/objects/{pk}/'.format(app_label=self.get_app_label(), model_name=self.get_model_name(), pk=self.get_model_pk())
        return ''

    def get_audit_trail_url(self):
        """returns the URL to display the audit trail for this model instance."""
        if self.get_model_inst():
            return '/audit_trail/{app_label}/{model_name}/{subject_identifier}/'.format(app_label=self.get_app_label(), model_name=self.get_model_name(), subject_identifier=self.get_model_inst().get_subject_identifier())
        return ''
