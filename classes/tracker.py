import logging
from datetime import datetime
from django.db.models import ForeignKey, OneToOneField, Max
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ImproperlyConfigured
from lab_clinic_api.models import ResultItem
from bhp_registration.models import RegisteredSubject
from bhp_lab_tracker.models import HistoryModel, HistoryModelError

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class LabTracker(object):
    """An abstract class to track or maintain a history of subject's lab result value from both the lab_clinic_api models ands protocol scheduled model(s).

    Required class attributes to be defined on the subclass:
        * resultitem_test_code: a tuple of test codes for reference to the :mod:`lab_clinic_api.result_item`.
          For example: ('ELISA', 'RELISA', 'DNAPCR')
        * tracker_test_code = a test code to use for results coming from a registered model.
          For example: 'HIV'
        * group_name = a label to group all records in the history model related to this class instance.
          For example: 'HIV'

    Optional class attributes to be defined on the subclass:
        * models: a tuple of tuples where the containing tuple defines (model_cls, value_attr, date_attr)

        .. note:: If models is not defined, the class will just track values in :mod:`lab_clinic_api.result_item`.
    """

    MODEL_CLS = 0
    VALUE_ATTR = 1
    DATE_ATTR = 2
    IDENTIFIER_ATTR = 3
    result_item_tpl = (ResultItem, 'result_item_value', 'result_item_datetime', 'result__order__order_identifier')

    def __init__(self):
        """If the user does not declare self.models, the tracker will just get what's in lab_clinic_api tables."""
        if not 'models' in dir(self):
            self.models = []
        if self.models:
            if not isinstance(self.models, list):
                raise ImproperlyConfigured('Class attribute \'models\' must be a list. Got {0}'.format(self.models))
            for tpl in self.models:
                if not isinstance(tpl, tuple):
                    raise ImproperlyConfigured('Class attribute \'models\' list must contain tuples (model_cls, value_attr, date_attr). Got {0}'.format(self.models))
        # self.models.append(self.add_result_item_tpl())

    def _get_display_map(self):
        return self.get_display_map_prep()

    def get_display_map_prep(self):
        """Returns a dictionary that may be used to map values for storage in the :class:`HistoryModel` to value formats used in :class:`ResultItem` model.

            Format {given this value: store this value}.

            This is useful if update_prep adds results that are not described in the same format as the :class:`ResultItem` model.

            For example:
                {'A': 'POS', 'B': NEG} will store POS and NEG given A, B. POS, NEG is how it is stored in the :class:`ResultItem` model.

            Also, the map is inverted to generate a string of values using this map returning 'AB' instead of 'POSNEG'.

            Users may override."""
        return None

    def get_default_value(self):
        """Returns the a value if None is available.

        Users should override"""
        return None

    def _get_value_map(self, model_name):
        """Maps an instance result value according to a configured map, if such a map exists."""
        # check model exists
        for model_tpl in self.models:
            model_cls = self._unpack_model_tpl(model_tpl, self.MODEL_CLS)
            if model_name == model_cls._meta.object_name.lower():
                return self.get_value_map_prep(model_name)
        return None

    def get_value_map_prep(self, model_name):
        """Users should override to use a custom map for a given tracker model."""
        return {}

    def update(self, subject_identifier):
        """Updates the HistoryModel with the subject's values found in any registered models and ResultItem."""
        if self.models:
            self._update_from_tracker_models(subject_identifier)
        self._update_from_result_item_model(subject_identifier)

    def update_all(self, supress_messages=True):
        tot = RegisteredSubject.objects.values('subject_identifier').all().count()
        for index, registered_subject in enumerate(RegisteredSubject.objects.values('subject_identifier').all()):
            if not supress_messages:
                logger.info('{0} / {1} ...updating {2}'.format(index, tot, registered_subject.get('subject_identifier')))
            self.update(registered_subject.get('subject_identifier'))

    def _unpack_model_tpl(self, model_tpl, index=None):
        """Unpacks and returns the model_tpl to always include identifier_attr, or, if index provided, returns just the one item."""
        if index in range(0, 4):
            retval = model_tpl[index]
        else:
            try:
                model_cls, value_attr, date_attr = model_tpl
                identifier_attr = None
            except ValueError:
                model_cls, value_attr, date_attr, identifier_attr = model_tpl
                identifier_attr = model_tpl[self.IDENTIFIER_ATTR]
            except:
                raise
            retval = (model_cls, value_attr, date_attr, identifier_attr)
        return retval

    def _get_source_identifier_value(self, instance, identifier_attr):
        if identifier_attr:
            # try to get an identifier for the value, usually only available for
            # values coming from lab_clinic_api.
            #dig into the instance's relations to get the identifier
            identifier_attr = identifier_attr.split('__')
            obj = instance
            for attr in identifier_attr:
                obj = getattr(obj, attr)
            source_identifier = unicode(obj)  # this should be a string
        else:
            source_identifier = instance.pk
        return source_identifier

    def update_with_tracker_instance(self, instance, model_tpl):
        """Updates the history model given a registered tracker model instance.

        .. note:: An instance from ResultItem may be sent from the signal. Do not automatically 
        accept it, first send it to check of the testcode is being tracked."""
        model_cls, value_attr, date_attr, identifier_attr = self._unpack_model_tpl(model_tpl)
        if not model_cls == instance.__class__:
            raise TypeError('Model tuple item \'model_cls\' {0} does not match instance class. Got {1}.'.format(model_cls, instance._meta.object_name.lower()))
        source_identifier = self._get_source_identifier_value(instance, identifier_attr)
        if isinstance(instance, ResultItem):
            history_model, created = self._update_from_result_item_instance(instance)
        else:
            history_model, created = self._update_history_model(
                instance._meta.object_name.lower(),
                source_identifier,
                instance.get_subject_identifier(),
                self._get_test_code(instance),
                self._get_tracker_result_value(instance, value_attr),
                self._get_tracker_result_datetime(instance, date_attr),
                )
        return history_model, created

    def delete_with_tracker_instance(self, instance, model_tpl):
        """Deletes a single instance from the HistoryModel."""
        model_cls, value_attr, date_attr, identifier_attr = self._unpack_model_tpl(model_tpl)
        if not model_cls == instance.__class__:
            raise TypeError('Model tuple item \'model_cls\' {0} does not match instance class. Got {1}.'.format(model_cls, instance._meta.object_name.lower()))
        source_identifier = self._get_source_identifier_value(instance, identifier_attr)
        HistoryModel.objects.filter(
            source=instance._meta.object_name.lower(),
            source_identifier=source_identifier,
            subject_identifier=instance.get_subject_identifier(),
            test_code=self._get_test_code(instance),
            value_datetime=self._get_tracker_result_datetime(instance, date_attr),
            ).delete()

    def _update_from_tracker_models(self, subject_identifier):
        """Loops through all registered tracker models and updates the history model.

        Excludes ResultItem
        """
        from bhp_visit_tracking.models import BaseVisitTracking
        result_item_cls = self.result_item_tpl[self.MODEL_CLS]
        for model_tpl in self.models:
            model_cls, value_attr, date_attr, identifier_attr = self._unpack_model_tpl(model_tpl)
            if model_cls != result_item_cls:
                for field in model_cls._meta.fields:
                    if isinstance(field, (ForeignKey, OneToOneField)):
                        if issubclass(field.rel.to, BaseVisitTracking):
                            query_string = '{visit_field}__appointment__registered_subject__subject_identifier'.format(visit_field=field.name)
                            break
                        if field.rel.to == RegisteredSubject:
                            query_string = 'registered_subject__subject_identifier'
                            break
                if not query_string:
                    raise TypeError(('Cannot determine link to subject_identifier. The model class {0} is'
                                    ' not a subclass of BasVisitTracking and nor does it have a relation to RegisteredSubject.').format(model_cls._meta.object_name))
                options = {query_string: subject_identifier}
                #options = {'registered_subject__subject_identifier': subject_identifier}
                queryset = model_cls.objects.filter(**options)
                #except:
                #    AttributeError('Lab Tracker model {0} must have a key to either a visit model or RegisteredSubject'.format(model._meta.object_name))
                for instance in queryset:
                    self.update_with_tracker_instance(instance, (model_cls, value_attr, date_attr))

    def _update_history_model(self, source, source_identifier, subject_identifier, test_code, value, value_datetime):
        """Inserts or Updates to the history model using get_or_create() with the given criteria."""
        # logger.info('          ...source {0}'.format(source))
        history_model, created = HistoryModel.objects.get_or_create(
            source=source,
            source_identifier=source_identifier,
            group_name=self._get_group_name(),
            subject_identifier=subject_identifier,
            test_code=test_code,
            value_datetime=value_datetime,
            defaults={'value': value, 'history_datetime': datetime.today()})
        if not created:
            history_model.value = value
            history_model.history_datetime = datetime.today()
            history_model.save()
        return history_model, created

    def _update_from_result_item_model(self, subject_identifier):
        """Updates the history model from values in ResultItem for this subject."""
        result_item_cls = self.result_item_tpl[self.MODEL_CLS]
        value_attr = self.result_item_tpl[self.VALUE_ATTR]
        date_attr = self.result_item_tpl[self.DATE_ATTR]
        identifier_attr = self.result_item_tpl[self.IDENTIFIER_ATTR]
        for result_item in result_item_cls.objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=self._get_resultitem_test_codes()):
            self._update_history_model('resultitem', self._get_source_identifier_value(result_item, identifier_attr), subject_identifier, result_item.test_code.code, getattr(result_item, value_attr), getattr(result_item, date_attr))

    def _update_from_result_item_instance(self, instance):
        """Updates the history model from values in ResultItem for this subject."""
        history_model, created = None, None
        if not isinstance(instance, self.result_item_tpl[self.MODEL_CLS]):
            raise TypeError('Expected instance to be an instance of ResultItem.')
        value_attr = self.result_item_tpl[self.VALUE_ATTR]
        date_attr = self.result_item_tpl[self.DATE_ATTR]
        identifier_attr = self.result_item_tpl[self.IDENTIFIER_ATTR]
        if instance.test_code.code in self._get_resultitem_test_codes():
            history_model, created = self._update_history_model(
                'resultitem',
                self._get_source_identifier_value(instance, identifier_attr),
                instance.get_subject_identifier(),
                instance.test_code.code,
                getattr(instance, value_attr),
                getattr(instance, date_attr))
        return history_model, created

    def _get_resultitem_test_codes(self):
        """Returns a tuple of test codes that appear in ResultItem and are of interest to this tracker."""
        if not self.resultitem_test_code:
            raise AttributeError('Class attribute \'resultitem_test_code\' cannot be None. Should be a test code or tuple of test codes.')
        if not isinstance(self.resultitem_test_code, (list, tuple)):
            self.resultitem_test_code = (self.resultitem_test_code, )
        return self.resultitem_test_code

    def _get_test_code(self, instance):
        if instance.__class__ == self.result_item_tpl[self.MODEL_CLS]:
            return instance.test_code.code
        else:
            return self._get_tracker_item_test_code()

    def _get_tracker_item_test_code(self):
        """Returns a user defined test code to use on results put together from a registered model."""
        if not self.tracker_test_code:
            raise AttributeError('Class attribute \'tracker_test_code\' cannot be None. Should be the test code used for tracker model results')
        return self.tracker_test_code

    def _get_group_name(self):
        """Returns a group_name or 'name' to group values in the history model for this class."""
        return self.group_name

    def _get_tracker_result_datetime(self, instance, date_attr=None):
        """Returns the datetime of the result item value determined either by getting the instance
        attribute or calling the instance method :func:`get_result_datetime` with the attribute name.

        Args:
            * date_attr: instance attribute name on instance that has the datetime (default: result_item_datetime)
        """
        if not date_attr:
            # default to attr name in result_item model
            date_attr = 'result_item_datetime'
        if 'get_result_datetime' in dir(instance):
            retval = instance.get_result_datetime(date_attr)
        else:
            retval = getattr(instance, date_attr)
        return retval

    def _get_tracker_result_value(self, instance, value_attr=None):
        """Returns a result item value which, if a map exists, is mapped to a value label that matches the tracker.

        Qualitative values must be translated / mapped to how they appear in ResultItem.

        Args:
            * value_attr: the instance attribute that holds the result item value. (default: result_item_value)
        """
        if not value_attr:
            # default to attr name in result_item model
            value_attr = 'result_item_value'
        # get the value either with getattr or instance.get_result_value()
        if 'get_result_value' in dir(instance):
            result_value = instance.get_result_value(value_attr)
        else:
            try:
                result_value = getattr(instance, value_attr)
            except:
                raise TypeError('Expected attribute \'{0}\' or method \'get_result_value()\' on instance {0}.'.format(value_attr, instance._meta.object_name))
        # get a result value map, if it exists
        result_value_map = self._get_value_map(instance._meta.object_name.lower())
        if result_value_map:
            retval = result_value_map.get(result_value)
        else:
            retval = result_value
        # fail if there is no return value
        if not retval:
            raise ValueError('Tracker value cannot be None. Instance value is {0}, map={1}'.format(result_value, result_value_map))
        return retval

    def get_history(self, subject_identifier, value_datetime, order_desc=False):
        """Returns values from the history model for this subject as an ordered queryset
        filtered for records on or before value_datetime."""
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        self.update(subject_identifier)
        return HistoryModel.objects.filter(
            subject_identifier=subject_identifier,
            value_datetime__lte=value_datetime,
            group_name=self._get_group_name()).order_by(order_by)

    def get_current_value(self, subject_identifier, value_datetime=None):
        history_model = self.get_current_instance(subject_identifier, value_datetime)
        if not history_model:
            retval = self.get_default_value()
        else:
            retval = history_model.value
        return retval

    def get_current_instance(self, subject_identifier, value_datetime=None):
        """Returns only the most current value if any exist in HistoryModel."""
        history_model = None
        max_value_datetime = None
        if not value_datetime:
            value_datetime = datetime.today()
        # get max value_datetime for this subject / test code
        if HistoryModel.objects.filter(
                subject_identifier=subject_identifier,
                value_datetime__lte=value_datetime,
                group_name=self._get_group_name()).exists():
            aggr = HistoryModel.objects.filter(
                subject_identifier=subject_identifier,
                value_datetime__lte=value_datetime,
                group_name=self._get_group_name()).aggregate(Max('value_datetime'))
            # change time on datetime to 00:00
            max_value_datetime = aggr.get('value_datetime__max', None)
        if not max_value_datetime:
            logger.warning('    nothing to do OR Max value datetime is None for {0} date {1}.'.format(subject_identifier, value_datetime))
        else:
            max_value_datetime = datetime(max_value_datetime.year, max_value_datetime.month, max_value_datetime.day, 0, 0)
            if HistoryModel.objects.filter(
                    subject_identifier=subject_identifier,
                    value_datetime__lte=value_datetime,
                    group_name=self._get_group_name(),
                    value_datetime=max_value_datetime).exists():
                try:
                    history_model = HistoryModel.objects.get(
                        subject_identifier=subject_identifier,
                        value_datetime__lte=value_datetime,
                        group_name=self._get_group_name(),
                        value_datetime=max_value_datetime)
                except MultipleObjectsReturned as e:
                    for history_model in HistoryModel.objects.filter(
                            subject_identifier=subject_identifier,
                            value_datetime__lte=value_datetime,
                            group_name=self._get_group_name(),
                            value_datetime=max_value_datetime):
                        self.log_history_model_error(history_model, e)
                    history_model.value = self.get_default_value()
                except:
                    raise
        return history_model

    def log_history_model_error(self, history_model, error):
        history_model_error = HistoryModelError()
        for field in history_model._meta.fields:
            if field.name not in ['id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']:
                setattr(history_model_error, field.name, getattr(history_model, field.name))
        history_model_error.error_message = error
        history_model_error.save()

    def get_history_as_list(self, subject_identifier):
        """Returns all values as a list in ascending chronological order."""
        queryset = self.get_history(subject_identifier, datetime.today())
        return [qs.value for qs in queryset]

    def get_history_as_string(self, subject_identifier, mapped=True):
        """Returns a subject's qualitative values joined as a string in ascending chronological order.

        If mapped is True and a display_map is defined, map is inverted and a string of values is generated from the map."""
        if not self._get_display_map():
            mapped = False
        retlst = []
        inv_display_map = {}
        lst = self.get_history_as_list(subject_identifier)
        if mapped:
            for k, v in self._get_display_map().iteritems():
                inv_display_map[v] = inv_display_map.get(v, [])
                inv_display_map[v].append(k)
        for l in lst:
            if mapped:
                retlst.append(inv_display_map[l][0].lower())
            else:
                retlst.append(l)
        return ''.join(retlst)
