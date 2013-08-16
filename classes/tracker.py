import logging
from datetime import datetime
from django.db.models import ForeignKey, OneToOneField, Max, get_model
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ImproperlyConfigured
#from lab_clinic_api.models import ResultItem
from bhp_registration.models import RegisteredSubject
from bhp_base_model.models import BaseModel
from bhp_lab_tracker.models import HistoryModel, HistoryModelError, DefaultValueLog

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
          Must be unique for each type of value being tracked. For example: 'HIV'.

    Optional class attributes to be defined on the subclass:
        * models: a tuple of tuples where the containing tuple defines (model_cls, value_attr, date_attr).
          Use this attribute to include models from your app that capture values not captured in
          model :class:`lab_clinic_api.models.ResultItem`.

        .. note:: If models is not defined, the class will just track values in :mod:`lab_clinic_api.result_item`.

    For example::

        class InfantHivLabTracker(HivLabTracker):
            models = [
                (HivTesting, 'pcr_result', 'pcr_date', None, True),
                (HivTesting, 'elisa_result', 'elisa_date', None, True)]
        lab_tracker.register(InfantHivLabTracker)

    You may also need to add a method on the model to return a known value. For example, for HIV::

        def get_result_value(self, attr=None):
            retval = None
            if not attr in dir(self):
                raise TypeError('Attribute {0} does not exist in model {1}'.format(attr, self._meta.object_name))
            if attr == 'is_hiv_pos':
                if self.is_hiv_pos.lower() == 'yes':
                    retval = 'POS'
                else:
                    retval = 'NEG'
            return retval
    """

    MODEL_CLS = 0
    VALUE_ATTR = 1
    DATE_ATTR = 2
    IDENTIFIER_ATTR = 3
    ALLOW_NULL = 4
    RESULT_ITEM_TPL = (('lab_clinic_api', 'resultitem'), 'result_item_value', 'result_item_datetime', 'result__order__order_identifier')
    models = None

    def __init__(self):
        """If the user does not declare self.models, the tracker will add result_item so that the
        tracker at least gets what's in lab_clinic_api tables.

        .. note:: ResultItem model is added by the :class:`SiteTracker` during register()"""
        self._result_item_tpl = None
        self._models = None
        #if self.models:
        #    self.set_models(self.models)

    @classmethod
    def add_model_tpl(self, model_tpl):
        if not isinstance(model_tpl, tuple):
            raise ImproperlyConfigured('Class attribute \'models\' list must contain tuples (model_cls, value_attr, date_attr). Got {0}'.format(model_tpl))
        if model_tpl not in self.models:
            self.models.append(model_tpl)

    def set_models(self, models=None):
        if models:
            if not isinstance(models, list):
                raise TypeError('Expected a list for parameter \'models\'.')
        self._models = models or []
        # add the default "result item" tuple, need this one at least
        if not self._get_result_item_tpl() not in self._models:
            self._models.append(self._get_result_item_tpl())

    def get_models(self):
        if not self._models:
            self.set_models()
        return self._models

    def set_result_item_tpl(self):
        APP_LABEL = 0
        MODEL_NAME = 1
        self._result_item_tpl = self.RESULT_ITEM_TPL
        if isinstance(self._result_item_tpl[self.MODEL_CLS], tuple):
            self._result_item_tpl[self.MODEL_CLS] = get_model(self._result_item_tpl[self.MODEL_CLS][APP_LABEL], self._result_item_tpl[self.MODEL_CLS][MODEL_NAME])
        if not issubclass(self._result_item_tpl[self.MODEL_CLS], BaseModel):
            raise TypeError('Expected a model class for the first item of the tracker tuple. Got {0}'.format(self._result_item_tpl[self.MODEL_CLS]))

    def _get_result_item_tpl(self, key=None):
        if not self._result_item_tpl:
            self.set_result_item_tpl()
        if not key == None:
            if key not in [self.MODEL_CLS, self.VALUE_ATTR, self.DATE_ATTR]:
                raise TypeError('KeyError. Expected [0,1,2]. Got{0}.'.format(key))
            return self._result_item_tpl[key]
        return self._result_item_tpl

    def get_result_item_model_cls(self):
        """Returns the model class for the model that has the result which is lab_clinic_api.models.result_item by default."""
        return self._get_result_item_tpl(self.MODEL_CLS)

    def get_result_item_value_attrname(self):
        return self._get_result_item_tpl(self.VALUE_ATTR)

    def get_result_item_date_attrname(self):
        return self._get_result_item_tpl(self.DATE_ATTR)

    def get_result_item_identifier_attrname(self):
        return self._get_result_item_tpl(self.IDENTIFIER_ATTR)

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

    def get_default_value(self, group_name, subject_identifier, value_datetime):
        """Returns the a value if None is available.

        Users should override"""
        return None

    def _get_default_value(self, group_name, subject_identifier, value_datetime):
        """Returns the default value when none is available from the HistoryModel."""
        default_value = self.get_default_value(group_name, subject_identifier, value_datetime)
        if not default_value:
            raise ImproperlyConfigured('Method get_default_value() must return a value. Got None.')
        else:
            # track that a default value was used
            subject_type = 'unknown'
            if RegisteredSubject.objects.filter(subject_identifier=subject_identifier):
                registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
                subject_type = registered_subject.subject_type
            self.log_default_value_used(group_name, subject_identifier, subject_type, value_datetime)
        return default_value

    def _get_value_map(self, model_name):
        """Maps an instance result value according to a configured map, if such a map exists."""
        # check model exists
        for model_tpl in self.get_models():
            model_cls = self.unpack_model_tpl(model_tpl, self.MODEL_CLS)
            if model_name == model_cls._meta.object_name.lower():
                return self.get_value_map_prep(model_name)
        return None

    def get_value_map_prep(self, model_name):
        """Users should override to use a custom map for a given tracker model."""
        return {}

    def update(self, subject_identifier):
        """Updates the HistoryModel with the subject's values found in any registered models and ResultItem."""
        if self.get_models():
            self._update_from_tracker_models(subject_identifier)
        self._update_from_result_item_model(subject_identifier)

    def update_all(self, supress_messages=True):
        tot = RegisteredSubject.objects.values('subject_identifier').all().count()
        for index, registered_subject in enumerate(RegisteredSubject.objects.values('subject_identifier').filter(subject_identifier__isnull=False)):
            if not supress_messages:
                logger.info('{0} / {1} ...updating {2}'.format(index, tot, registered_subject.get('subject_identifier')))
            self.update(registered_subject.get('subject_identifier'))
        return tot

    @classmethod
    def unpack_model_tpl(self, model_tpl, index=None):
        """Unpacks and returns the model_tpl to always include identifier_attr, or, if index provided, returns just the one item.

        Size of tuple may vary depending on the options provided.

        .. note:: the first element, the model_cls, may be a tuple of (app_label, model_name).

        .. seealso:: :func:`_get_tracker_result_value` for expalnation of `allow_null`.
        """
        if index in range(0, 5):
            retval = model_tpl[index]
            if index == 0:
                if isinstance(model_tpl[index], tuple):
                    retval = get_model(model_tpl[index][0], model_tpl[index][1])
        else:
            allow_null = False
            identifier_attr = None
            try:
                model_cls, value_attr, date_attr = model_tpl
                if isinstance(model_cls, tuple):
                    model_cls = get_model(model_cls[0], model_cls[1])
            except ValueError:
                try:
                    model_cls, value_attr, date_attr, identifier_attr = model_tpl
                    if isinstance(model_cls, tuple):
                        model_cls = get_model(model_cls[0], model_cls[1])
                    identifier_attr = model_tpl[self.IDENTIFIER_ATTR]
                    if identifier_attr:
                        if not isinstance(identifier_attr, basestring):
                            raise TypeError('Model tuple element \'identifier_attr\' must be a string.')
                except ValueError:
                    model_cls, value_attr, date_attr, identifier_attr, allow_null = model_tpl
                    if isinstance(model_cls, tuple):
                        model_cls = get_model(model_cls[0], model_cls[1])
                    #identifier_attr = model_tpl[self.IDENTIFIER_ATTR]
                    if identifier_attr:
                        if not isinstance(identifier_attr, basestring):
                            raise TypeError('Model tuple element \'identifier_attr\' must be a string.')
                    #allow_null = model_tpl[self.ALLOW_NULL]
            except:
                raise
            retval = (model_cls, value_attr, date_attr, identifier_attr, allow_null)
        return retval

    def _get_source_identifier_value(self, instance, identifier_attr):
        if identifier_attr:
            # try to get an identifier for the value, usually only available for
            # values coming from lab_clinic_api.
            # dig into the instance's relations to get the identifier
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
                  accept it, first send it to check if the testcode is being tracked.
        """
        history_model = None
        created = False
        model_cls, value_attr, date_attr, identifier_attr, allow_null = self.unpack_model_tpl(model_tpl)
        if not model_cls == instance.__class__:
            raise TypeError('Model tuple item \'model_cls\' {0} does not match instance class. Got {1}.'.format(model_cls, instance._meta.object_name.lower()))
        source_identifier = self._get_source_identifier_value(instance, identifier_attr)
        if isinstance(instance, self.get_result_item_model_cls()):
            # will return nothing if the test code is not being tracked.
            history_model, created = self._update_from_result_item_instance(instance)
        else:
            result_value = self._get_tracker_result_value(instance, value_attr, allow_null=allow_null)
            value_datetime = self._get_tracker_result_datetime(instance, date_attr)
            report_datetime = instance.get_report_datetime()
            test_code = self._get_test_code(instance, value_attr=value_attr)
            if result_value and value_datetime:
                history_model, created = self._update_history_model(
                    instance._meta.object_name.lower(),
                    source_identifier,
                    instance.get_subject_identifier(),
                    test_code,
                    result_value,
                    value_datetime,
                    report_datetime,
                    )
            else:
                self.delete_with_tracker_source(instance, source_identifier, test_code)
        return history_model, created

    def delete_with_tracker_source(self, instance, source_identifier, test_code):
        """Deletes a history model instance for this source and source identifier.

        Called if the source data has changed and is now not complete enough for an update."""
        if HistoryModel.objects.filter(test_code=test_code, source_identifier=source_identifier, source=instance._meta.object_name.lower()).exists():
            HistoryModel.objects.get(test_code=test_code, source_identifier=source_identifier, source=instance._meta.object_name.lower()).delete()

    def delete_with_tracker_instance(self, instance, model_tpl):
        """Deletes a single instance from the HistoryModel."""
        model_cls, value_attr, date_attr, identifier_attr, allow_null = self.unpack_model_tpl(model_tpl)
        if not model_cls == instance.__class__:
            raise TypeError('Model tuple item \'model_cls\' {0} does not match instance class. Got {1}.'.format(model_cls, instance._meta.object_name.lower()))
        source_identifier = self._get_source_identifier_value(instance, identifier_attr)
        HistoryModel.objects.filter(
            source=instance._meta.object_name.lower(),
            source_identifier=source_identifier,
            subject_identifier=instance.get_subject_identifier(),
            test_code=self._get_test_code(instance, value_attr=value_attr),
            value_datetime=self._get_tracker_result_datetime(instance, date_attr),
            ).delete()

    def _update_from_tracker_models(self, subject_identifier):
        """Loops through all registered tracker models and updates the history model.

        Excludes ResultItem
        """
        from bhp_visit_tracking.models import BaseVisitTracking
        query_string = None
        for model_tpl in self.get_models():
            query_string = None
            model_cls, value_attr, date_attr, identifier_attr, allow_null = self.unpack_model_tpl(model_tpl)
            if model_cls != self.get_result_item_model_cls():
                for field in model_cls._meta.fields:
                    if isinstance(field, (ForeignKey, OneToOneField)):
                        if issubclass(field.rel.to, BaseVisitTracking):
                            query_string = '{visit_field}__appointment__registered_subject__subject_identifier'.format(visit_field=field.name)
                            break
                        if field.rel.to == RegisteredSubject:
                            query_string = 'registered_subject__subject_identifier'
                            break
                if not query_string:
                    if 'get_subject_identifier' in dir(model_cls):
                        query_string = 'subject_identifier'
                if not query_string:
                    raise TypeError(('Cannot determine link to subject_identifier. The model class {0} is'
                                    ' not a subclass of BaseVisitTracking and nor does it have a relation to RegisteredSubject.').format(model_cls._meta.object_name))
                options = {query_string: subject_identifier}
                #options = {'registered_subject__subject_identifier': subject_identifier}
                queryset = model_cls.objects.filter(**options)
                #except:
                #    AttributeError('Lab Tracker model {0} must have a key to either a visit model or RegisteredSubject'.format(model._meta.object_name))
                for instance in queryset:
                    self.update_with_tracker_instance(instance, (model_cls, value_attr, date_attr, identifier_attr, allow_null))

    def _update_history_model(self, source, source_identifier, subject_identifier, test_code, value, value_datetime, report_datetime):
        """Inserts or Updates to the history model using get_or_create() with the given criteria."""
        history_model, created = HistoryModel.objects.get_or_create(
            source=source,
            source_identifier=source_identifier,
            test_code=test_code,
            group_name=self.get_group_name(),
            subject_identifier=subject_identifier,
            value_datetime=value_datetime,
            defaults={'value': value, 'history_datetime': datetime.today(), 'report_datetime': report_datetime})
        if not created:
            history_model.value = value
            history_model.history_datetime = datetime.today()
            history_model.report_datetime = report_datetime
            history_model.save()
        return history_model, created

    def _update_from_result_item_model(self, subject_identifier):
        """Updates the history model from values in ResultItem for this subject."""
        for result_item in self.get_result_item_model_cls().objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=self._get_resultitem_test_codes()):
            report_datetime = result_item.get_report_datetime()
            self._update_history_model(
                'resultitem',
                self._get_source_identifier_value(result_item, self.get_result_item_identifier_attrname()),
                subject_identifier,
                result_item.test_code.code,
                getattr(result_item, self.get_result_item_value_attrname()),
                getattr(result_item, self.get_result_item_date_attrname()),
                report_datetime)

    def _update_from_result_item_instance(self, instance):
        """Updates the history model from values in ResultItem for this subject."""
        history_model, created = None, None
        if not isinstance(instance, self.get_result_item_model_cls()):
            raise TypeError('Expected instance to be an instance of ResultItem.')
        if instance.test_code.code in self._get_resultitem_test_codes():
            history_model, created = self._update_history_model(
                'resultitem',
                self._get_source_identifier_value(instance, self.get_result_item_identifier_attrname()),
                instance.get_subject_identifier(),
                instance.test_code.code,
                getattr(instance, self.get_result_item_value_attrname()),
                getattr(instance, self.get_result_item_date_attrname()),
                instance.get_report_datetime())
        return history_model, created

    def _get_resultitem_test_codes(self):
        """Returns a tuple of test codes that appear in ResultItem and are of interest to this tracker."""
        if not self.resultitem_test_code:
            raise AttributeError('Class attribute \'resultitem_test_code\' cannot be None. Should be a test code or tuple of test codes.')
        if not isinstance(self.resultitem_test_code, (list, tuple)):
            self.resultitem_test_code = (self.resultitem_test_code, )
        return self.resultitem_test_code

    def _get_test_code(self, instance, **kwargs):
        """Returns test_code for this value by inspecting the model instance or defers to the default."""
        if instance.__class__ == self.get_result_item_model_cls():
            return instance.test_code.code
        elif 'get_test_code' in dir(instance):
            value_attr = kwargs.get('value_attr', None)
            if not value_attr:
                raise AttributeError('Expected a value for kwarg \'value_attr\'. Got None. Needed for model {0}: method get_test_code().'.format(instance._meta.object_name))
            return instance.get_test_code(kwargs.get('value_attr', None))
        else:
            return self._get_tracker_item_test_code()

    def _get_tracker_item_test_code(self):
        """Returns a user defined test code to use on results put together from a registered model."""
        if not self.tracker_test_code:
            raise AttributeError('Class attribute \'tracker_test_code\' cannot be None. Should be the test code used for tracker model results')
        return self.tracker_test_code

    def get_group_name(self, group_name=None):
        """Returns a group_name or 'name' to group values in the history model for this class."""
        if group_name:
            if group_name != self.group_name:
                raise TypeError('Group name must be {0}. Got {1}'.format(self.group_name, group_name))
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
        #if isinstance(retval, date):
        #    raise
        return retval

    def _get_tracker_result_value(self, instance, value_attr=None, **kwargs):
        """Returns a result item value which, if a map exists, is mapped to a value label that matches the tracker.

        Qualitative values must be translated / mapped to how they appear in ResultItem.

        Args:
            * value_attr: the instance attribute that holds the result item value. (default: result_item_value)

        Kwargs:
            * allow_null: if True, will not throw an error if the source model returns a None. For example, source model may have
              skip logic that leaves the field value as None.

        """
        allow_null = kwargs.get('allow_null', False)
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
        if not retval and not allow_null:
            raise ValueError('Tracker value cannot be None. Instance value is {0}, map={1}'.format(result_value, result_value_map))
        return retval

    def get_history(self, group_name, subject_identifier, value_datetime, order_desc=False):
        """Returns values from the history model for this subject as an ordered queryset
        filtered for records on or before value_datetime."""
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        self.update(subject_identifier)
        return HistoryModel.objects.filter(
            subject_identifier=subject_identifier,
            value_datetime__lte=value_datetime,
            group_name=self.get_group_name(group_name)).order_by(order_by)

    def get_current_value(self, group_name, subject_identifier, value_datetime=None):
        """Returns the current value relative to value_datetime or the default value if there is no
        information for this subject in the History model."""
        is_default = False
        history_model = self.get_current_instance(self.get_group_name(group_name), subject_identifier, value_datetime)
        if not history_model:
            # nothing found in model, return a default value
            retval = self._get_default_value(group_name, subject_identifier, value_datetime)
            is_default = True
        else:
            retval = history_model.value
        return (retval, is_default)

    def get_current_instance(self, group_name, subject_identifier, value_datetime=None):
        """Returns the instance of :class:`bhp_lab_tracker.models.HistoryModel` with the most current value if it exists."""
        history_model = None
        max_value_datetime = None
        if not value_datetime:
            value_datetime = datetime.today()
        # drop time for the query
        query_value_datetime = datetime(value_datetime.year, value_datetime.month, value_datetime.day, 23, 59, 59, 999)
        # get max value_datetime for this subject / test code
        if HistoryModel.objects.filter(
                subject_identifier=subject_identifier,
                value_datetime__lte=query_value_datetime,
                group_name=self.get_group_name(group_name)).exists():
            aggr = HistoryModel.objects.filter(
                subject_identifier=subject_identifier,
                value_datetime__lte=query_value_datetime,
                group_name=self.get_group_name(group_name)).aggregate(Max('value_datetime'))
            max_value_datetime = aggr.get('value_datetime__max', None)
        if not max_value_datetime:
            logger.warning('    no history found for {0} date {1} for group {2}.'.format(subject_identifier, query_value_datetime, group_name))
        else:
            max_value_datetime = datetime(max_value_datetime.year, max_value_datetime.month, max_value_datetime.day, max_value_datetime.hour, max_value_datetime.minute, max_value_datetime.second, max_value_datetime.microsecond)
            if HistoryModel.objects.filter(
                    subject_identifier=subject_identifier,
                    group_name=self.get_group_name(group_name),
                    value_datetime=max_value_datetime).exists():
                try:
                    history_model = HistoryModel.objects.get(
                        subject_identifier=subject_identifier,
                        group_name=self.get_group_name(group_name),
                        value_datetime=max_value_datetime)
                except MultipleObjectsReturned as e:
                    # multiple objects resturned, if each has the same value, then no harm
                    # otherwise log an error and return the default value
                    values = []
                    for history_model in HistoryModel.objects.filter(
                            subject_identifier=subject_identifier,
                            group_name=self.get_group_name(group_name),
                            value_datetime=max_value_datetime):
                        values.append(history_model.value)
                    if not len(list(set(values))) == 1:
                        # more than one value for the same value_datetime, log the error!
                        self.log_history_model_error(history_model, e)
                        history_model.value = self._get_default_value(group_name, subject_identifier, value_datetime)
                except:
                    raise
        return history_model

    def log_default_value_used(self, group_name, subject_identifier, subject_type, value_datetime=None):
        """Logs that a default value was used. """
        default_value_log = DefaultValueLog.objects.create(
            subject_identifier=subject_identifier,
            subject_type=subject_type,
            group_name=group_name,
            value_datetime=value_datetime)
        return default_value_log

    def log_history_model_error(self, history_model, error):
        """Logs errors with the HistoryModel such as when no instance can be found for a subject."""
        history_model_error = HistoryModelError()
        for field in history_model._meta.fields:
            if field.name not in ['id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']:
                setattr(history_model_error, field.name, getattr(history_model, field.name))
        history_model_error.error_message = error
        history_model_error.save()

    def get_history_as_list(self, subject_identifier, reference_datetime=None):
        """Returns all values on or before :attr:`reference_datetime` for a subject as a list in ascending chronological order."""
        if not reference_datetime:
            reference_datetime = datetime.today()
        if not self.group_name:
            raise ImproperlyConfigured('Class attribute \'group_name\' cannot be None.')
        queryset = self.get_history(self.group_name, subject_identifier, reference_datetime)
        return [qs.value for qs in queryset]

    def get_history_as_string(self, subject_identifier, mapped=True):
        """Returns a subject's qualitative values joined as a string in ascending chronological order.

        Args:
            * subject_identifier:
            * mapped: if False do not attempt to use a display map (default=True).

        If :attr:`mapped` is True and a display map is defined in :func:`get_display_map_prep`, the display map is
        inverted and a string of values is generated from the map."""
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
