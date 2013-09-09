import inspect
from datetime import datetime
from bhp_lab_tracker.models import HistoryModel


class HistoryUpdater(object):

    def __init__(self, model_inst, group_name, subject_type, tracker=None, tracked_test_codes=None):
        """Updates the HistoryModel model class with values from a model instance.

            Args:
                model_inst: a model instance that meets the requirements for a lab_tracker (see site_lab_tracker register()).
                group_name: the LabTracker group name, just used as a reference value for the HistoryModel.
                tracker: a valid tracker (namedtuple) instance (Default:None). Required for calls to :func:`update`
                tracker_test_codes: a list of test codes that the caller (labTracker) is monitoring (Default:None). Required for calls to :func:`update`
        """
        self._model_inst = None
        self._tracker = None
        self._value = None
        self._value_datetime = None
        self._subject_identifier = None
        self._subject_type = None
        self._test_code = None
        self._group_name = None
        self.set_model_inst(model_inst)
        self.set_group_name(group_name)
        self.set_subject_type(subject_type)
        self._tracked_test_codes = tracked_test_codes
        if tracker:
            self.set_tracker(tracker)

    def set_model_inst(self, value=None):
        """Sets the model instance that is used to set most instance attributes and to update the HistoryModel."""
        self._model_inst = value
        if not self._model_inst:
            raise TypeError('self._model_inst may not be None.')

    def get_model_inst(self):
        if not self._model_inst:
            self.set_model_inst()
        return self._model_inst

    def set_tracker(self, value=None):
        """Sets the tracker provided by the caller which has information on how to inspect the model instance."""
        self._tracker = value
        if not self._tracker:
            raise TypeError('self._tracker may not be None.')

    def get_tracker(self):
        if not self._tracker:
            self.set_tracker()
        return self._tracker

    def set_group_name(self, value=None):
        """Sets the group name provided by the caller which is only needed as a reference field value for the HistoryModel."""
        self._group_name = value
        if not self._group_name:
            raise TypeError('self._group_name may not be None.')

    def get_group_name(self):
        if not self._group_name:
            self.set_group_name()
        return self._group_name

    def set_value(self):
        """Sets the result value from the model instance."""
        self._value = None
        if 'get_result_value' in dir(self.get_model_inst()):
            self._value = self._get_method(self.get_model_inst().get_result_value, 'attr', self.get_tracker().value_attr)
        else:
            try:
                self._value = getattr(self.get_model_inst(), self.get_tracker().value_attr)
            except:
                raise TypeError('Cannot get result value from instance. Expected model attribute \'{0}\' or method \'get_result_value()\' on instance {0}.'.format(self.get_tracker().value_attr, self.get_model_inst()._meta.object_name))

    def get_value(self):
        if not self._value:
            self.set_value()
        return self._value

    def set_value_datetime(self):
        """Sets the result datetime by accessing a method or field attribute on the model instance."""
        self._value_datetime = None
        if 'get_result_datetime' in dir(self.get_model_inst()):
            self._value_datetime = self._get_method(self.get_model_inst().get_result_datetime, 'attr', self.get_tracker().value_attr)
        else:
            self._value_datetime = getattr(self.get_model_inst(), self.get_tracker().datetime_attr)
        if not self._value_datetime:
            raise TypeError('self._value_datetime may not be None.')

    def get_value_datetime(self):
        if not self._value_datetime:
            self.set_value_datetime()
        return self._value_datetime

    def set_subject_identifier(self):
        """Sets the subject identifier by accessing the method get_subject_identifier on the model instance."""
        self._subject_identifier = None
        if 'get_subject_identifier' in dir(self.get_model_inst()):
            self._subject_identifier = self.get_model_inst().get_subject_identifier()
        if not self._subject_identifier:
            raise TypeError('self._subject_identifier may not be None.')

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def set_subject_type(self, value=None):
        """Sets the subject type by accessing the method get_subject_type or the subject_type attr on the model instance."""
        self._subject_type = value
#         if not self.
#         if 'get_subject_type' in dir(self.get_model_inst()):
#             self._subject_type = self.get_model_inst().get_subject_type()
#         else:
#             self._subject_type = self.get_model_inst().subject_type
        if not self._subject_type:
            raise TypeError('self._subject_type may not be None.')

    def get_subject_type(self):
        if not self._subject_type:
            self.set_subject_type()
        return self._subject_type

    def set_test_code(self):
        """Sets the test_code for this value by inspecting the model instance.

        model instance method :func:`get_test_code` may return a test code conditional to the tracker.value_attr.

        model instance method :func:`get_test_code` may specify parameter \'attr\'. All other parameters will be ignored.
        """
        self._test_code = None
        if 'get_test_code' in dir(self.get_model_inst()):
            self._test_code = self._get_method(self.get_model_inst().get_test_code, 'attr', self.get_tracker().value_attr)
        if not self._test_code:
            raise TypeError('Cannot determine the test code for model {0}. Perhaps add a get_test_code(self) or get_test_code(self, attr) method to the model. '.format(self.get_model_inst()))

    def get_test_code(self):
        if not self._test_code:
            self.set_test_code()
        return self._test_code

    def get_tracked_test_codes(self):
        """Gets the list of test codes to inspect the model instance.

            * If a model instance test code is not listed then the save is aborted.
            * Comes from the calling lab_tracker."""

        return self._tracked_test_codes

    def update(self):
        """Updates the history model given a registered tracker model instance.

        .. note:: Default values are not saved to the history model.

        .. note:: An instance from ResultItem may be sent from the signal. Do not automatically
                  accept it, first send it to check if the testcode is being tracked.
        """
        history_model = None
        # if model instance test code is not listed with this lab tracker, abort
        if not self.get_test_code() in self.get_tracked_test_codes():
            return None
        # the instance must be listed as a model with the passed tracker
        if not self.get_tracker().model_cls == self.get_model_inst().__class__:
            raise TypeError('Model {0} in tracker tuple does not match instance class. Got {1}.'.format(self.get_tracker().model_cls, self.get_model_inst()._meta.object_name.lower()))
        if self.get_value() and self.get_value_datetime():
            # update the history model, get or create
            history_model, created = HistoryModel.objects.get_or_create(
                source_app_label=self.get_model_inst()._meta.app_label,
                source_identifier=self.get_model_inst().pk,
                test_code=self.get_test_code(),
                group_name=self.get_group_name(),
                subject_identifier=self.get_subject_identifier(),
                subject_type=self.get_subject_type(),
                value_datetime=self.get_value_datetime(),
                defaults={'value': self.get_value(),
                          'history_datetime': datetime.today(),
                          'report_datetime': self.get_model_inst().get_report_datetime(),
                          'source_model_name': self.get_model_inst()._meta.object_name.lower()})
            if not created:
                history_model.value = self.get_value()
                history_model.history_datetime = datetime.today()
                history_model.report_datetime = self.get_model_inst().get_report_datetime()
                history_model.source_model_name = self.get_model_inst()._meta.object_name.lower()
                history_model.save()
        else:
            self.delete()
        return history_model

    def delete(self):
        """Deletes a single instance from the HistoryModel."""
        HistoryModel.objects.filter(
            source_app_label=self.get_model_inst()._meta.app_label,
            source_model_name=self.get_model_inst()._meta.object_name.lower(),
            source_identifier=self.get_model_inst().pk,
            group_name=self.get_group_name(),
            ).delete()

    def _get_method(self, func, parameter_name, parameter_value):
        """Calls the given func with or without a value depending on inspection."""
        argspec = inspect.getargspec(func)
        if parameter_name in argspec.args:
            return func(parameter_value)
        else:
            return func()
