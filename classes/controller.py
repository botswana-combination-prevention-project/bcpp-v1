import logging
import copy
from datetime import datetime
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
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

    To register a class or classes create :file:`lab_tracker.py` in your module and add something like this:

    .. code-block:: python

        from bhp_lab_tracker.classes import site_lab_tracker
        from bhp_lab_tracker.classes import HivLabTracker
        from models import HivTestReview, HivResult


        class SubjectHivLabTracker(HivLabTracker):

            trackers = [(HivTestReview, 'recorded_hiv_result', 'hiv_test_date', ),
                      (HivResult, 'hiv_result', 'hiv_result_datetime', )]

        site_lab_tracker.register(SubjectHivLabTracker)

    .. seealso:: :class:`HivLabTracker`

    """
    def __init__(self):
        self._registry = []
        self._group_names = []
        self._autodiscovered = None
        self._models = None

    def register(self, lab_tracker_cls):
        """Registers lab_tracker classes to the registry (a list).

        Ensures model classes refered to by the trackers in the LabTracker classes have the following methods:
            * get_subject_identifier
            * get_report_datetime
            * get_result_datetime
            * get_test_code
        """
        lab_tracker_inst = lab_tracker_cls()
        if lab_tracker_cls in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % lab_tracker_cls)
        if (lab_tracker_cls.subject_type, lab_tracker_cls.group_name) in [(cls.subject_type, cls.group_name) for cls in self._registry]:
            raise AlreadyRegistered('A lab_tracker with subject_type=={0} and group_name=={1} is already registered. Cannot register {2}.'.format(lab_tracker_cls.subject_type, lab_tracker_cls.group_name, lab_tracker_cls))
        if 'subject_type' not in dir(lab_tracker_cls):
            raise ImproperlyConfigured('Missing class attribute \'subject_type\'. See tracker {0}.'.format(lab_tracker_cls))
        if not 'SUBJECT_TYPES' in dir(settings):
            raise ImproperlyConfigured('Missing settings attribute SUBJECT_TYPES.')
        if lab_tracker_inst.get_subject_type() not in settings.SUBJECT_TYPES and not lab_tracker_inst.get_subject_type() == 'test_subject_type':
            raise ImproperlyConfigured('Class attribute \'subject_type\' must be a valid subject type. Got {0}. Must be one of {1}. See tracker {2}'.format(lab_tracker_inst.get_subject_type(), settings.SUBJECT_TYPES, lab_tracker_cls))
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
        # all trackers in a LabTracker must be namedtuples
        # TODO: is this check necessary, aren't these converted when instantiated?
        for tracker in lab_tracker_cls().get_trackers():
            if not isinstance(tracker, TrackerNamedTpl):
                raise TypeError('expected an instance of TrackerTpl. Got {0}'.format(tracker))
        self._registry.append(lab_tracker_cls)

    def unregister(self, lab_tracker_cls):
        for index, cls in enumerate(self._registry):
            if lab_tracker_cls == cls:
                del self._registry[index]

    def update_history(self, model_inst):
        """Updates history for a given model instance (on pk) via the tracker for the model class."""
        for lab_tracker_cls in self._registry:
            lab_tracker_inst = lab_tracker_cls(model_inst.get_subject_identifier())
            if isinstance(model_inst, lab_tracker_inst.get_models()):
                for tracker in lab_tracker_inst.get_trackers():
                    if tracker.model_cls == model_inst.__class__:
                        HistoryUpdater(model_inst, lab_tracker_inst.get_group_name(), lab_tracker_inst.get_subject_type(), tracker, lab_tracker_inst._get_tracked_test_codes()).update()

    def delete_history(self, model_inst):
        """Deletes history for a given model instance (on pk) via the tracker for the model class."""
        for lab_tracker_cls in self._registry:
            lab_tracker_inst = lab_tracker_cls(model_inst.get_subject_identifier())
            if isinstance(model_inst, lab_tracker_inst.get_models()):
                HistoryUpdater(model_inst, lab_tracker_inst.get_group_name(), lab_tracker_inst.get_subject_type()).delete()

    def update_history_for_all(self, supress_messages=None):
        """Updates the history for all subjects in RegisteredSubject for all LabTrackers in the registry."""
        RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
        tot = RegisteredSubject.objects.values('subject_identifier').all().count()
        for lab_tracker_cls in self._registry:
            for index, registered_subject in enumerate(RegisteredSubject.objects.values('subject_identifier').filter(subject_identifier__isnull=False)):
                if not supress_messages:
                    logger.info('{0} / {1} ...updating {2}'.format(index, tot, registered_subject.get('subject_identifier')))
                lab_tracker_inst = lab_tracker_cls(registered_subject.get('subject_identifier'))
                lab_tracker_inst.update_history()
        return (index, tot)

    def all(self):
        """Returns the registry as a list."""
        return self._registry

    def _get_lab_tracker_inst_by_group_name(self, group_name, subject_identifier, subject_type):
        """Returns a lab_tracker instantiated for this subject from the registry given a group_name and subject_type."""
        lab_tracker_inst = None
        for lab_tracker_cls in self._registry:
            inst = lab_tracker_cls(subject_identifier)
            if inst.get_group_name() == group_name and inst.get_subject_type() == subject_type:
                lab_tracker_inst = inst
                break
        return lab_tracker_inst

    def set_model_list(self):
        """Sets the list of model classes used by the trackers in the registry."""
        self.confirm_autodiscovered()
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

    def get_history_as_qs(self, group_name, subject_identifier, subject_type, reference_datetime=None):
        """Returns the result history as QuerySet."""
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier, subject_type)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history(reference_datetime)
        return retval

    def get_history_as_list(self, group_name, subject_identifier, subject_type, reference_datetime=None):
        """Returns the result history as a list of values."""
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier, subject_type)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history_as_list(reference_datetime)
        return retval

    def get_history_as_string(self, group_name, subject_identifier, subject_type, mapped=None, reference_datetime=None):
        """Returns the result history as a string of values."""
        self.confirm_autodiscovered()
        retval = ''
        if not reference_datetime:
            reference_datetime = datetime.today()
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier, subject_type)
        if lab_tracker_inst:
            retval = lab_tracker_inst.get_history_as_string(reference_datetime, mapped)
        return retval

    def get_current_value(self, group_name, subject_identifier, subject_type):
        """Wraps :func:`get_value` calling with value_datetime = today's date."""
        return self.get_value(group_name, subject_identifier, subject_type, value_datetime=datetime.today())

    def get_value(self, group_name, subject_identifier, subject_type, value_datetime=None):
        """Returns the result value or a tuple with the result value, if default, in this LabTracker group for this subject.
 
        Searches thru the registry to find a class that can be used to search for the value..
 
            Args:
                * group_name: group name as set on the LabTracker class declaration
                * subject_identifier: a valid subject identifier
                * value_datetime: a valid datetim
 
        .. note:: If a default value is returned, the result is a tuple.
 
       This method will be called from any class that needs the value being tracked. For example,
       :class:`ClinicGradeFlag` needs to know the HIV Status of a subject at the time a sample
       was drawn in order to grade a test result.
 
       .. seealso:: :func:`lab_clinic_reference.classes.ClinicGradeFlag.get_hiv_status`.
 
        """
        self.confirm_autodiscovered()
        value = None
        is_default_value = None  # if no value is found in the classes' history model, is there a default?
        if subject_type not in settings.SUBJECT_TYPES and not subject_type == 'test_subject_type':
            raise ImproperlyConfigured('Invalid subject type \'{0}\'. Must be one of {1}. See settings.py.'.format(subject_type, settings.SUBJECT_TYPES))
        lab_tracker_inst = self._get_lab_tracker_inst_by_group_name(group_name, subject_identifier, subject_type)
        if lab_tracker_inst:
            value = lab_tracker_inst.get_value(value_datetime)
            is_default_value = lab_tracker_inst.get_is_default_value()
        else:
            raise ImproperlyConfigured('Could not find a lab_tracker instance for group_name \'{0}\' and subject_identifier \'{1}\'. Available classes are {2}'.format(group_name, subject_identifier, self._registry))
        if not value:
            # a value should always be returned, even if it is the classes' default value.
            raise TypeError('Value cannot be None. Using ({0}, {1}, {2}). Lab tracker class not found for group name or no get_default_value() method.'.format(group_name, subject_identifier, value_datetime))
        if is_default_value:
            return (value, 'default')
        return value

    def autodiscover(self):
        """Searches all apps for :file:`lab_tracker.py` and registers all :class:`LabTracker` subclasses found."""
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(site_lab_tracker._registry)
                import_module('%s.lab_tracker' % app)
            except:
                site_lab_tracker._registry = before_import_registry
                if module_has_submodule(mod, 'lab_tracker'):
                    raise

    def set_autodiscovered(self, value=None):
        if value:
            self._autodiscovered = value

    def get_autodiscovered(self):
        if not self._autodiscovered:
            self.set_autodiscovered()
        return self._autodiscovered

    def confirm_autodiscovered(self):
        return True
#         """Confirms that autodiscover() was called at least once."""
#         if not self.get_autodiscovered():
#             raise ImproperlyConfigured('Call lab_tracker.autodiscover() before accessing values. Perhaps place this in the urls.py')


# A global to contain all lab_tracker instances from modules
site_lab_tracker = Controller()
