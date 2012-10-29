import copy
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SiteLabTracker(object):
    """Registers from modules with a lab_tracker module (lab_tracker.py).

    Models in the models tuples class attribute
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

    def register(self, lab_tracker_cls):
        """Registers lab_tracker classes to a list.

        .. note:: :mod:`lab_clinic_api`'s model :class:`ResultItem` is always added to :attr:`models` of the incoming
                  lab_tracker_cls before appending to the register.
        """
        if lab_tracker_cls in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % lab_tracker_cls)
        # confirm the models in the models class attribute have the required methods.
        if 'models' in dir(lab_tracker_cls):
            for model_tpl in lab_tracker_cls.models:
                model_cls = lab_tracker_cls()._unpack_model_tpl(model_tpl, lab_tracker_cls.MODEL_CLS)
                if 'get_subject_identifier' not in dir(model_cls):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. '
                                               'Define the method \'get_subject_identifier()\' on '
                                               'the model first.'.format(model_cls._meta.object_name))
        else:
            lab_tracker_cls.models = []
        # add result_item model
        lab_tracker_cls.models.append(lab_tracker_cls.result_item_tpl)
        self._registry.append(lab_tracker_cls)
        # check group_names of registered classes to enforce uniqueness across classes.
        for cls in self._registry:
            if cls == lab_tracker_cls:
                if cls().get_group_name != lab_tracker_cls().get_group_name():
                    raise ImproperlyConfigured('{0} group name must be unique across LabTracker classes. '
                                               'Group name {1} also appears in .'.format(lab_tracker_cls.__name__,
                                                                                         lab_tracker_cls().get_group_name(),
                                                                                         cls.__name__))

    def update_all(self, supress_messages):
        for lab_tracker_cls in self._registry:
            lab_tracker_cls().update_all(supress_messages)

    def all(self):
        return self._registry

    def get_value(self, group_name, subject_identifier, value_datetime):
        """Searches thru the registry to find a class that can be used to search for the value.

            Args:
                * group_name: the group name that you expect to be the same as that of lab_tracker_cls().get_group_name()
                * subject_identifier: used by :func:`get_current_value`
                * value_datetime: used by :func:`get_current_value`

           Method :finc:`get_value()`

           This method will be called from any class that needs the value being tracked. For example,
           :class:`ClinicGradeFlag` needs to know the HIV Status of a subject at the time a sample
           was drawn in order to grade a test result.
           See :func:`lab_clinic_reference.classes.ClinicGradeFlag.get_hiv_status`.
        """
        value = None
        is_default_value = None  # if no value is found in the classes' history model, is there a default?
        for lab_tracker_cls in self._registry:
            # confirm group names match
            if lab_tracker_cls().get_group_name() == group_name:
                value, is_default_value = lab_tracker_cls().get_current_value(group_name, subject_identifier, value_datetime)
            if value:
                break
        if not value:
            # a value should always be returned, even if it is the classes' default value.
            raise TypeError('Value cannot be None. Using ({0}, {1}, {2})'.format(group_name, subject_identifier, value_datetime))
        return (subject_identifier, value, value_datetime, is_default_value)

    def autodiscover(self):
        """Searches all apps for :file:`lab_tracker.py` and registers and :class:`LabTracker` subclasses found."""
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(lab_tracker._registry)
                import_module('%s.lab_tracker' % app)
            except:
                lab_tracker._registry = before_import_registry
                if module_has_submodule(mod, 'lab_tracker'):
                    raise
# A global to contain all lab_tracker instances from modules
lab_tracker = SiteLabTracker()
