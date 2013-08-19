import logging
import copy
from datetime import datetime
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from bhp_lab_tracker.exceptions import LabTrackerError
from helpers import TrackerNamedTpl
from history_updater import HistoryUpdater

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):
    """Registers from modules with a lab_tracker module (lab_tracker.py).

    Models in the trackers tuples class attribute
      1. must define the method :func:`get_subject_identifier`.
      2. may define:
           * :func:`get_result_value(attr)`
           * :func:`get_result_datetime(attr)`

    To register a class or classes create :file:`lab_tracker.py` in your module and add something like this:

    .. code-block:: python

        from bhp_lab_tracker.classes import lab_tracker
        from bhp_lab_tracker.classes import HivLabTracker


        class InfantHivLabTracker(HivLabTracker):
            pass
        lab_tracker.register(InfantHivLabTracker)

    .. seealso:: :class:`HivLabTracker`

    """
    def __init__(self):
        self._registry = []
        self._group_names = []
        self.autodiscovered = False
        self._models = None

    def register(self, lab_tracker_cls):
        """Registers lab_tracker classes to a list."""
        lab_tracker_inst = lab_tracker_cls()
        if lab_tracker_cls in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % lab_tracker_cls)
        if 'trackers' in dir(lab_tracker_cls):
            for tracker in lab_tracker_inst.get_trackers():
                if 'get_subject_identifier' not in dir(tracker.model_cls):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. '
                                               'Define the method \'get_subject_identifier()\' on '
                                               'the model first.'.format(tracker.model_cls._meta.object_name))
                if 'get_report_datetime' not in dir(tracker.model_cls):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. '
                                               'Define the method \'get_report_datetime()\' on '
                                               'the model first.'.format(tracker.model_cls._meta.object_name))
                if 'get_result_datetime' not in dir(tracker.model_cls):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. '
                                               'Define the method \'get_result_datetime()\' on '
                                               'the model first.'.format(tracker.model_cls._meta.object_name))
                if 'get_test_code' not in dir(tracker.model_cls):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. '
                                               'Define the method \'get_test_code()\' on '
                                               'the model first.'.format(tracker.model_cls._meta.object_name))
        else:
            if 'models' in dir(lab_tracker_cls):
                raise ImproperlyConfigured('Class attribute \'models\' has been changed to \'trackers\'. Please correct your class declaration for lab_tracker {0}'.format(lab_tracker_cls))
            raise ImproperlyConfigured('LabTracker class {0} is missing class attribute \'trackers\'.'.format(lab_tracker_cls))

        for tracker in lab_tracker_cls().get_trackers():
            if not isinstance(tracker, TrackerNamedTpl):
                raise TypeError('expected an instance of TrackerTpl. Got {0}'.format(tracker))
        self._registry.append(lab_tracker_cls)

    def update(self, model_inst):
        """Updates the history model for the tracker that refers to this model."""
        for lab_tracker_cls in self._registry:
            lab_tracker_inst = lab_tracker_cls(model_inst.get_subject_identifier())
            if isinstance(model_inst, lab_tracker_inst.get_models()):
                for tracker in lab_tracker_inst.get_trackers():
                    if tracker.model_cls == model_inst.__class__:
                        HistoryUpdater(model_inst, lab_tracker_inst.get_group_name(), tracker, lab_tracker_inst._get_tracked_test_codes()).update()

    def delete_history(self, model_inst):
        for lab_tracker_cls in self._registry:
            lab_tracker_inst = lab_tracker_cls(model_inst.get_subject_identifier())
            if isinstance(model_inst, lab_tracker_inst.get_models()):
                HistoryUpdater(model_inst, lab_tracker_inst.get_group_name()).delete_history()

    def update_all(self, supress_messages):
        RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
        tot = RegisteredSubject.objects.values('subject_identifier').all().count()
        for lab_tracker_cls in self._registry:
            for index, registered_subject in enumerate(RegisteredSubject.objects.values('subject_identifier').filter(subject_identifier__isnull=False)):
                if not supress_messages:
                    logger.info('{0} / {1} ...updating {2}'.format(index, tot, registered_subject.get('subject_identifier')))
                lab_tracker_inst = lab_tracker_cls(registered_subject.get('subject_identifier'))
                lab_tracker_inst.update_history(supress_messages)

#     def update_history_for_all(self, supress_messages=True):
#         tot = RegisteredSubject.objects.values('subject_identifier').all().count()
#         for index, registered_subject in enumerate(RegisteredSubject.objects.values('subject_identifier').filter(subject_identifier__isnull=False)):
#             if not supress_messages:
#                 logger.info('{0} / {1} ...updating {2}'.format(index, tot, registered_subject.get('subject_identifier')))
#             self.update_history(registered_subject.get('subject_identifier'))
#         return tot

    def all(self):
        return self._registry

    def _get_lab_tracker_inst_by_group_name(self, group_name, subject_identifier):
        lab_tracker_inst = None
        for lab_tracker_cls in self._registry:
            inst = lab_tracker_cls(subject_identifier)
            if inst.get_group_name() == group_name:
                lab_tracker_inst = inst
                break
        return lab_tracker_inst

    def set_model_list(self):
        if not self.autodiscovered:
            raise LabTrackerError('Lab Tracker is not ready. Call autodiscover first.')
        self._models = []
        for lab_tracker_cls in self._registry:
            lab_tracker_inst = lab_tracker_cls()
            self._models.extend(lab_tracker_inst.get_models())
        self._models = tuple(self._models)

    def get_model_list(self):
        """Returns a list of model classes used by the trackers in the registry."""
        if not self._models:
            self.set_model_list()
        return self._models

    def get_history_as_qs(self, group_name, subject_identifier, reference_datetime=None):
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history(reference_datetime)
        return retval

    def get_history_as_list(self, group_name, subject_identifier, reference_datetime=None):
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history_as_list(reference_datetime)
        return retval

    def get_history_as_string(self, group_name, subject_identifier, mapped=True, reference_datetime=None):
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history_as_string(reference_datetime, mapped)
        return retval

    def get_current_value(self, group_name, subject_identifier):
        return self.get_value(group_name, subject_identifier, value_datetime=datetime.today())

    def get_value(self, group_name, subject_identifier, value_datetime=None):
        """Searches thru the registry to find a class that can be used to search for the value.

            Args:
                * group_name: the group name that you expect to be the same as that of lab_tracker_cls().get_group_name()
                * subject_identifier: used by :func:`get_current_value`
                * value_datetime: used by :func:`get_current_value`

           Method :func:`get_value()`

           This method will be called from any class that needs the value being tracked. For example,
           :class:`ClinicGradeFlag` needs to know the HIV Status of a subject at the time a sample
           was drawn in order to grade a test result.
           See :func:`lab_clinic_reference.classes.ClinicGradeFlag.get_hiv_status`.
        """
        self.confirm_autodiscovered()
        value = None
        is_default_value = None  # if no value is found in the classes' history model, is there a default?
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier)
        if lab_tracker_inst:
            value = lab_tracker_inst.get_value(value_datetime)
            is_default_value = lab_tracker_inst.get_is_default_value()
        if not value:
            # a value should always be returned, even if it is the classes' default value.
            raise TypeError('Value cannot be None. Using ({0}, {1}, {2}). Lab tracker class not found for group name or no get_default_value() method.'.format(group_name, subject_identifier, value_datetime))
        if is_default_value:
            return (value, 'default')
        return value

    def autodiscover(self):
        """Searches all apps for :file:`lab_tracker.py` and registers and :class:`LabTracker` subclasses found."""
        if not self.autodiscovered:
            self.autodiscovered = True
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_lab_tracker._registry)
                    import_module('%s.lab_tracker' % app)
                except:
                    site_lab_tracker._registry = before_import_registry
                    if module_has_submodule(mod, 'lab_tracker'):
                        raise

    def confirm_autodiscovered(self):
        """Confirms that autodiscover() was called at least once."""
        if not self.autodiscovered:
            raise ImproperlyConfigured('Call lab_tracker.autodiscover() before accessing values. Perhaps place this in the urls.py')


# A global to contain all lab_tracker instances from modules
site_lab_tracker = Controller()
