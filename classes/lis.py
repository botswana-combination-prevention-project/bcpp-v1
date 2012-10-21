import logging
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import ForeignKey
from bhp_poll_mysql.poll_mysql import PollMySQL
from bhp_research_protocol.models import Protocol
from lab_receive.models import Receive as LisReceive
from lab_aliquot.models import Aliquot as LisAliquot
from lab_order.models import Order as LisOrder
from lab_result.models import Result as LisResult
from lab_result_item.models import ResultItem as LisResultItem
from bhp_registration.models import RegisteredSubject
from lab_clinic_api.models import Receive, Aliquot, Order, Result, ResultItem
from lab_clinic_api.models import AliquotType, AliquotCondition
from lab_import_lis.models import LisImportError
from import_history import ImportHistory
from convert_lis_attr import ConvertLisAttr


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Lis(object):

    """ Import from django-lis"""
    def __init__(self, db, **kwargs):
        self.db = db

    def update_from_lis(self, subject_identifier):
        """ Update the Edc labs for a given subject_identifier from the Lis."""
        poll_mysql = PollMySQL(db=self.db)
        if poll_mysql.is_server_active():
            import_history = ImportHistory(self.db, subject_identifier)
            import_history.force_release(subject_identifier)
            return self.import_from_lis(subject_identifier=subject_identifier)
        return None

    def import_from_lis(self, **kwargs):
        """Imports data from the django-lis for each model in the relational model including list
        models.

        The relational model is :class:`Receive` > :class:`Aliquot` > :class:`Order` >
        :class:`Result` > :class:`ResultItem`
        List models are panel, test_code, aliquot_type, aliquot_condition

        Using "func:`get_or_create`, if instances do not exist they will be created.

        If the source patient identifier cannot be linked to an instance of registered
        subject, the data is not imported and an error is loggged in model :class:`LisImportError`.

        Note: List models on the target (edc) are not the same models as source. That is list models
        on target come from :mod:`lab_clinic_api` and on source come from lab_panel, lab_aliquot_list, etc.
        For example target.panel != source.panel yet the attribute values of panel instance on
        target and source are the same (see isinstance() test for ForeignKey fields below).
        """

        subject_identifier = kwargs.get('subject_identifier', None)
        protocol_identifier = kwargs.get('protocol_identifier', None)

        lock_name = subject_identifier
        if not lock_name:
            if 'LAB_LOCK_NAME' in dir(settings):
                lock_name = settings.LAB_LOCK_NAME
            else:
                lock_name = protocol_identifier
        import_history = ImportHistory(self.db, lock_name)
        if import_history.start():
            # import all received
            modified_aliquots = []
            modified_orders = []
            modified_results = []
            if subject_identifier:
                logger.info('  subject identifier specified: "{0}"'.format(subject_identifier))
                registered_subject = RegisteredSubject.objects.get(subject_identifier__iexact=unicode(subject_identifier))
                if import_history.last_import_datetime:
                    qset = Q()
                    q = (Q(modified__gte=import_history.last_import_datetime) | Q(created__gte=import_history.last_import_datetime))
                    qset.add(q, Q.AND)
                    modified_aliquots = self._get_modified(LisAliquot, self.db, 'aliquot_identifier', qset, Q(receive__patient=registered_subject.subject_identifier))
                    qset = Q()
                    qset.add(q, Q.AND)
                    modified_orders = self._get_modified(LisOrder, self.db, 'order_identifier', qset, Q(aliquot__receive__patient=registered_subject.subject_identifier))
                    qset = Q()
                    qset.add(q, Q.AND)
                    modified_results = self._get_modified(LisResult, self.db, 'result_identifier', qset, Q(order__aliquot__receive__patient=registered_subject.subject_identifier))
                qset = Q(patient__subject_identifier=registered_subject.subject_identifier)
            elif protocol_identifier:
                protocol = Protocol.objects.using(self.db).get(protocol_identifier__iexact=protocol_identifier)
                if import_history.last_import_datetime:
                    qset = Q()
                    q = (Q(modified__gte=import_history.last_import_datetime) | Q(created__gte=import_history.last_import_datetime))
                    qset.add(q, Q.AND)
                    modified_aliquots = self._get_modified(LisAliquot, self.db, 'aliquot_identifier', qset, Q(receive__protocol=protocol))
                    qset = Q()
                    qset.add(q, Q.AND)
                    modified_orders = self._get_modified(LisOrder, self.db, 'order_identifier', qset, Q(aliquot__receive__protocol=protocol))
                    qset = Q()
                    qset.add(q, Q.AND)
                    modified_results = self._get_modified(LisResult, self.db, 'result_identifier', qset, Q(order__aliquot__receive__protocol=protocol))
                qset = Q(protocol=protocol)
            else:
                qset = Q()
            # start by filtering at the top of the relational model with Receive and
            # adding and/or updating anything down the cascade
            if import_history.last_import_datetime:
                qset.add((Q(modified__gte=import_history.last_import_datetime) | Q(created__gte=import_history.last_import_datetime)), Q.AND)
            total = LisReceive.objects.using(self.db).filter(qset).count()
            n = 0
            logger.info('Preparing initial receive query...')
            for lis_receive in LisReceive.objects.using(self.db).filter(qset).order_by('receive_datetime'):
                n += 1
                if not import_history.locked:
                    # lock was deleted by another user
                    break
                logger.info('{0} / {1} Receiving {receive_identifier} for '
                            '{subject_identifier}'.format(n, total, receive_identifier=lis_receive.receive_identifier,
                                                          subject_identifier=lis_receive.patient.subject_identifier))
                registered_subject = self._registered_subject_handler(lis_receive, Receive, 'receive_identifier')
                if registered_subject:
                    receive = self._import_model(lis_receive, Receive, 'receive_identifier', exclude_fields=None, registered_subject=registered_subject)
                    for lis_aliquot in LisAliquot.objects.using(self.db).filter(receive__receive_identifier=receive.receive_identifier):
                        aliquot = self._import_model(lis_aliquot, Aliquot, 'aliquot_identifier',
                                                     exclude_fields=None, receive=receive)
                        if aliquot:
                            try:
                                modified_aliquots.remove(aliquot.aliquot_identifier)
                            except ValueError:
                                pass
                            for lis_order in LisOrder.objects.using(self.db).filter(aliquot__aliquot_identifier=aliquot.aliquot_identifier):
                                order = self._import_model(lis_order, Order, 'order_identifier',
                                                           exclude_fields=None, aliquot=aliquot)
                                if order:
                                    try:
                                        modified_orders.remove(order.order_identifier)
                                    except ValueError:
                                        pass
                                    for lis_result in LisResult.objects.using(self.db).filter(order__order_identifier=order.order_identifier):
                                        result = self._import_model(lis_result, Result, 'result_identifier',
                                                                    exclude_fields=None, order=order)
                                        if result:
                                            try:
                                                modified_results.remove(result.result_identifier)
                                            except ValueError:
                                                pass
                                            for lis_result_item in LisResultItem.objects.using(self.db).filter(result__result_identifier=result.result_identifier, validation_status='F'):
                                                # only importing where validation_status='F'.
                                                self._import_result_item_model(lis_result_item, result)
                                            # update order status
                                            order.save()
            # update any left in the modified lists that were not included above
            # since the receive record was not modified
            logger.info('Checking for data modified after the receiving instances...')
            logger.info('    Aliquots...')
            for lis_aliquot in LisAliquot.objects.using(self.db).filter(aliquot_identifier__in=modified_aliquots):
                if Receive.objects.filter(receive_identifier=lis_aliquot.receive.receive_identifier):
                    receive = Receive.objects.get(receive_identifier=lis_aliquot.receive.receive_identifier)
                    aliquot = self._import_model(lis_aliquot, Aliquot, 'aliquot_identifier',
                                                 exclude_fields=None, receive=receive)
                    if aliquot.aliquot_condition.pk == '10':
                        TypeError('Invalid ')
                    modified_aliquots.remove(aliquot.aliquot_identifier)
            logger.info('    Orders...')
            for lis_order in LisOrder.objects.using(self.db).filter(order_identifier__in=modified_orders):
                if Aliquot.objects.filter(aliquot_identifier=lis_order.aliquot.aliquot_identifier):
                    aliquot = Aliquot.objects.get(aliquot_identifier=lis_order.aliquot.aliquot_identifier)
                    order = self._import_model(lis_order, Order, 'order_identifier',
                                               exclude_fields=None, aliquot=aliquot)
                    modified_orders.remove(order.order_identifier)
            logger.info('    Results and ResultItems...')
            for lis_result in LisResult.objects.using(self.db).filter(result_identifier__in=modified_results):
                if Order.objects.filter(order_identifier=lis_result.order.order_identifier):
                    order = Order.objects.get(order_identifier=lis_result.order.order_identifier)
                    result = self._import_model(lis_result, Result, 'result_identifier',
                                                exclude_fields=None, order=order)
                    modified_results.remove(result.result_identifier)
                    for lis_result_item in LisResultItem.objects.using(self.db).filter(result__result_identifier=result.result_identifier):
                        self._import_result_item_model(lis_result_item, result)
        self.delete_pending_orphans(subject_identifier=subject_identifier)
        return import_history.finish()

    def _import_model(self, lis_source, target_cls, target_identifier_name, exclude_fields, **kwargs):
        """ Transfers values between two models for matching attributes.

        Arguments:
          * lis_source: source model
          * target_cls: model class for target
          * target_identifier_name: field name represented by a unique value such as
            an identifier result_identifier, order_identifier, etc. Used by get_or_create
            to decide to get or create an instance.
          * exclude_fields: a custom list of field names to ignore. default(['id'])

        Keyword Arguments:
          * <fieldname>: any field name value pair. Use this to set the target attribute to a
            value other than that in the source model.

        Assumes model instance are identical except for foreignkeys and any fields listed
        in excluded fields. """
        options = {}
        defaults = {}
        target = None
        if not exclude_fields:
            # import_datetime does not exist in Lis models
            exclude_fields = ['id', 'import_datetime']
        else:
            exclude_fields.append('id')
            exclude_fields.append('import_datetime')
        custom_fields = ['registered_subject']
        list_fields = ['panel', 'aliquot_type', 'aliquot_condition']
        lis_source_fields = [field.name for field in lis_source._meta.fields]
        for field in target_cls._meta.fields:
            if field.default == NOT_PROVIDED:
                value = None
            else:
                value = field.default
            if field.name not in exclude_fields:
                if kwargs.get(field.name, None):
                    value = kwargs.get(field.name)
                elif field.name in list_fields:
                    value = self._get_or_create_list_field_instance(field.name, getattr(lis_source, field.name))
                elif field.name in custom_fields:
                    value = self._target_field_custom_handler(lis_source, target_cls, target_identifier_name, field)
                else:
                    # target value is source value for this attribute
                    if field.name in lis_source_fields:
                        value = getattr(lis_source, field.name)
                        if isinstance(value, ForeignKey):
                            raise TypeError('ForeignKey instances on source are not of the same class as FK instances on target.')
                defaults.update({field.name: value})
        defaults.update({'import_datetime': datetime.today()})
        options.update({'defaults': defaults})
        options.update({target_identifier_name: getattr(lis_source, target_identifier_name)})
        try:
            target, created = target_cls.objects.get_or_create(**options)
            if created:
                logger.info('    created {0} {1}'.format(target._meta.object_name, target))
            else:
                # get_or_create did a get, so update the instance with 'defaults' dict
                defaults = options.get('defaults')
                for field in target._meta.fields:
                    # exclude the only key field (identifier) plus others
                    if field.name in [fld_name for fld_name in defaults.iterkeys() if fld_name not in ['id', 'created', 'user_created', 'hostname_created', target_identifier_name]]:
                        setattr(target, field.name, defaults.get(field.name))
                target.save()
                logger.info('    updated {0} {1}'.format(target._meta.object_name, target))
        except MultipleObjectsReturned as e:
            self._add_or_remove_warning(lis_source, target_cls, target_identifier_name, e)
        except:
            raise
        return target

    def _import_result_item_model(self, lis_result_item, result):
        """ Imports from result_items from source to target.

        'tartget_cls' is in module lab_clinic_api and not lab_result_item.
        Do not use value for result, test_code from 'lis_result_item' as it is
        of the wrong class.  On 'target_cls' the attributes refer to instances in
        lab_clinic_api.

        Also, 'tartget_cls' does not have a \'result_item_identifier\' attr
        and instead uses a result instance as its key."""
        options = {}
        defaults = {}
        target_cls = ResultItem
        list_fields = ['test_code']
        for field in target_cls._meta.fields:
            if field.name not in ['id', 'result', 'test_code', 'import_datetime']:
                if field.name in list_fields:
                    value = self._get_or_create_list_field_instance(field.name, getattr(lis_result_item, field.name))
                else:
                    value = getattr(lis_result_item, field.name)
                defaults.update({field.name: value})
            if field.name == 'test_code':
                test_code = self._get_or_create_list_field_instance(field.name, getattr(lis_result_item, 'test_code'))
        defaults.update({'import_datetime': datetime.today()})
        options.update({'defaults': defaults})
        options.update({'result': result, 'test_code': test_code})
        target, created = target_cls.objects.get_or_create(**options)
        if created:
            logger.info('    created {0} {1}'.format(target._meta.object_name, target))
        else:
            # get_or_create did a get, so update the instance with 'defaults' dict
            defaults = options.get('defaults')
            for field in target._meta.fields:
                # exclude the key fields ('result', 'test_code') plus others
                if field.name in [fld_name for fld_name in defaults.iterkeys() if fld_name not in ['id', 'created', 'user_created', 'hostname_created', 'result', 'test_code']]:
                    setattr(target, field.name, defaults.get(field.name))
            target.save()
            logger.info('    updated {0} {1}'.format(target._meta.object_name, target))
        return target

    def _get_or_create_list_field_instance(self, name, lis_obj):
        obj = None
        convert_lis_attr = ConvertLisAttr()
        if lis_obj:
            if name == 'panel':
                obj, created = convert_lis_attr.panel(lis_obj)
                if created:
                    logger.info('    created panel {0}'.format(obj.name))
            elif name == 'test_code':
                obj, created = convert_lis_attr.test_code(lis_obj)
                if created:
                    logger.info('    created test_code {0}'.format(obj.code))
            elif name == 'aliquot_type':
                obj, created = AliquotType.objects.get_or_create(name=lis_obj.name, alpha_code=lis_obj.alpha_code, numeric_code=lis_obj.numeric_code)
                if created:
                    logger.info('    created aliquot_type {0}'.format(obj.name))
            elif name == 'aliquot_condition':
                obj, created = AliquotCondition.objects.get_or_create(name=lis_obj.name, short_name=lis_obj.short_name)
                if created:
                    logger.info('    created aliquot_condition {0}'.format(obj.name))
            else:
                raise TypeError('Unknown list name. Got {0}'.format(name))
            if not created:
                logger.info('    {0} exists, found {1}'.format(name, obj))
        return obj

    def _target_field_custom_handler(self, lis_source, target_cls, target_identifier_name, field):
        """ Handles a field and value in a custom manner. """
        value = None
        if field.name == 'registered_subject':
            self._registered_subject_handler(lis_source, target_cls, target_identifier_name)
        return value

    def _registered_subject_handler(self, lis_source, target_cls, target_identifier_name):
        """ Returns a registered_subject instance or none and updates the error log."""
        value = None
        if RegisteredSubject.objects.filter(subject_identifier=lis_source.patient.subject_identifier).exists():
            if RegisteredSubject.objects.filter(subject_identifier=lis_source.patient.subject_identifier).count() == 1:
                value = RegisteredSubject.objects.get(subject_identifier=lis_source.patient.subject_identifier)
                self._add_or_remove_warning(lis_source, target_cls, target_identifier_name, None)
            else:
                warning = ('warning: {target_identifier} has multiple subject identifiers '
                           '{subject_identifier}').format(target_identifier=getattr(lis_source, target_identifier_name),
                                                  subject_identifier=lis_source.patient.subject_identifier)
                self._add_or_remove_warning(lis_source, target_cls, target_identifier_name, warning)
        else:
            warning = ('warning: {target_identifier} has an unknown subject identifier '
                   '{subject_identifier}').format(target_identifier=getattr(lis_source, target_identifier_name),
                                                  subject_identifier=lis_source.patient.subject_identifier)
            self._add_or_remove_warning(lis_source, target_cls, target_identifier_name, warning)
        return value

    def _add_or_remove_warning(self, lis_source, target_cls, target_identifier_name, warning=None):
        """ Logs an error message or removes a previously logged message.

        An existing message is deleted if identifier matches and warning is None.

        Note: so far this is always a receive instance where identifier is the receive_identifier."""

        if warning:
            try:
                LisImportError.objects.get_or_create(
                    model_name=target_cls()._meta.object_name,
                    identifier=getattr(lis_source, target_identifier_name),
                    subject_identifier='-',
                    error_message=warning)
            except MultipleObjectsReturned as e:
                warning = 'MultipleObjectsReturned: {0} ({1})'.format(e, warning)
                LisImportError.objects.get_or_create(
                    model_name=target_cls()._meta.object_name,
                    identifier=getattr(lis_source, target_identifier_name)[0],
                    subject_identifier='-',
                    error_message=warning)
            except Exception as e:
                warning = 'Exception: {0} ({1})'.format(e, warning)
                LisImportError.objects.get_or_create(
                    model_name=target_cls()._meta.object_name,
                    identifier=target_identifier_name,
                    subject_identifier='-',
                    error_message=warning)
            logger.warning('  {0}'.format(warning))
        else:
            LisImportError.objects.filter(identifier=getattr(target_cls(), target_identifier_name)).delete()

    def _get_modified(self, model, using, identifier_name, qset, q):
        """ Returns a list of identifiers for instances that match the criteria qset."""
        modified = []
        _qset = qset
        _qset.add(q, Q.AND)
        for instance in model.objects.using(using).filter(_qset):
            modified.append(getattr(instance, identifier_name))
        return modified

    def delete_pending_orphans(self, **kwargs):
        """ Deletes pending orders where a complete order has come in but with a different order identifier for the same receive, panel and order_idenifier.

        Assumption is that there is only one order for a given receive identifier, order panel and order date.

        Will not delete an order that has a result.

        The dmis re-identifies orders/results if unvalidated then re-validated. In this case, the EDC
        will,, upon import, end up with two order instances and maybe two result instances for a single "result". Only one result instance will have
        resultitem instances. The now orphaned order and result instances have status Pending and New respectively.
        Since they no longer exist in the DMIS, they need to be deleted.
        """
        options = {'status': 'Pending'}
        if kwargs.get('subject_identifier', None):
            options.update({'subject_identifier': kwargs.get('subject_identifier')})
        orders = Order.objects.filter(**options).order_by('aliquot__receive__receive_identifier')
        tot = orders.count()
        logger.info('Scanning {0} pending orders to be removed if complete ...'.format(tot))
        m = 0
        ri_tot = ResultItem.objects.filter(validation_status__iexact='P').count()
        if ri_tot > 0:
            ResultItem.objects.filter(validation_status__iexact='P').delete()
            logger.info('    removed {0} preliminary result items...'.format(ri_tot))
        for order in orders:
            if Order.objects.filter(aliquot__receive=order.aliquot.receive, panel=order.panel, order_datetime=order.order_datetime, status__iexact='complete').exists():
                results = Result.objects.filter(order=order)
                if not results:
                    # no result so just delete the order.
                    m += 1
                    order.delete()
                else:
                    for result in results:
                        if not ResultItem.objects.filter(result=result).exists():
                            # no result items left, so delete the result and order.
                            m += 1
                            result.delete()
                            order.delete()
                        else:
                            logger.warning('Warning: \'Final\' result items exist for a \'New\' result, cannot remove \'Pending\' order {0}.'.format(order.order_identifier))
        logger.info('    removed {0} pending orders.'.format(m))
