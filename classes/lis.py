import logging
from django.db.models import Q
from bhp_research_protocol.models import Protocol
from lab_receive.models import Receive as LisReceive
from lab_aliquot.models import Aliquot as LisAliquot
from lab_order.models import Order as LisOrder
from lab_result.models import Result as LisResult
from lab_result_item.models import ResultItem as LisResultItem
from bhp_registration.models import RegisteredSubject
from lab_clinic_api.models import Receive, LisImportError, Aliquot, Order, Result, ResultItem
from lab_clinic_api.models import Panel, TestCode, AliquotType, AliquotCondition
from import_history import ImportHistory


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Lis(object):

    """ Import from django-lis"""
    def __init__(self, db, **kwargs):
        self.db = db

    def import_from_lis(self, protocol_identifier=None, **kwargs):

        import_history = ImportHistory(self.db, kwargs.get('subject_identifier', None) or protocol_identifier)
        if import_history.start():
            # import all received
            protocol = Protocol.objects.using(self.db).get(protocol_identifier__iexact=protocol_identifier)
            qset = Q(protocol=protocol)
            #if import_history.last_import_datetime:
            #    qset.add((Q(modified__gte=import_history.last_import_datetime) | Q(created__gte=import_history.last_import_datetime)), Q.AND)

            for lis_receive in LisReceive.objects.using(self.db).filter(qset):
                if not import_history.locked:
                    # lock was deleted by another user
                    break
                logger.info('Receiving {receive_identifier} for '
                            '{subject_identifier}'.format(receive_identifier=lis_receive.receive_identifier,
                                                          subject_identifier=lis_receive.patient.subject_identifier))
                receive = self._import_model(lis_receive, Receive(), 'receive_identifier', exclude_fields=None)
                for lis_aliquot in LisAliquot.objects.using(self.db).filter(receive__receive_identifier=receive.receive_identifier):
                    for aliquot in self._import_model(lis_aliquot, Aliquot(), 'aliquot_identifier', exclude_fields=None):
                        for lis_order in LisOrder.objects.using(self.db).filter(aliquot__aliquot_identifier=aliquot.aliquot_identifier):
                            for order in self._import_model(lis_order, Order(), 'order_identifier', exclude_fields=None):
                                for lis_result in LisResult.objects.using(self.db).filter(order__order_identifier=order.order_identifier):
                                    for result in self._import_model(lis_result, Result(), 'result_identifier', exclude_fields=None):
                                        for lis_result_item in LisResultItem.objects.using(self.db).filter(result__result_identifier=result.result_identifier):
                                            self._import_model(lis_result_item, ResultItem(), 'result_item_identifier', exclude_fields=None)
        import_history.finish()
        return None

    def _import_model(self, lis_source, target, target_identifier_name, exclude_fields):
        """ Imports from source model and sets and saves, to target, all fields except those excluded.

        Assumes model instance are identical except for excluded fields """
        if not exclude_fields:
            exclude_fields = ['id']
        else:
            exclude_fields.append('id')
        custom_fields = ['registered_subject']
        list_fields = ['panel', 'aliquot_type', 'aliquot_condition']
        for field in target._meta.fields:
            if field.name not in ['id']:
                if field.name in custom_fields:
                    value = self._target_field_custom_handler(lis_source, target, target_identifier_name, field)
                elif field.name in list_fields:
                    value = self._get_or_create_list_field_instance(field.name, getattr(lis_source, field.name))
                else:
                    value = getattr(lis_source, field.name)
            setattr(target, field.name, value)
        target.save()
        return target

    def _get_or_create_list_field_instance(self, name, lis_obj):
        obj = None
        if name == 'panel':
            #test_code
            test_code = TestCode.objects.get_or_create(code=lis_obj.test_code.code)[0]
            #aliquot_type
            aliquot_type = AliquotType.objects.get_or_create(name=lis_obj.aliquot_type.name)[0]
            #panel
            obj = Panel.objects.get_or_create(panel__name=lis_obj.name,
                                                       test_code=test_code,
                                                       aliquot_type=aliquot_type)[0]
        elif name == 'aliquot_type':
            obj = AliquotType.objects.get_or_create(name=lis_obj.aliquot_type.name)[0]
        elif name == 'aliquot_condition':
            obj = AliquotCondition.objects.get_or_create(name=lis_obj.aliquot_condition.name)[0]
        else:
            raise TypeError('Unknown list name. Got {0}'.format(name))
        return obj

    def _target_field_custom_handler(self, lis_source, target, target_identifier_name, field):
        """ Handles a field in a custom manner. """
        value = None
        if field.name == 'registered_subject':
            # only 'receive' has registered subject, so this code is
            # also specific to those source and target models
            if RegisteredSubject.objects.filter(subject_identifier=lis_source.patient.subject_identifier):
                value = RegisteredSubject.objects.get(subject_identifier=lis_source.patient.subject_identifier)
                if value is None:
                    warning = ('warning: {target_identifier} has an unknown subject identifier '
                           '{subject_identifier}').format(target_identifier=getattr(lis_source, target_identifier_name),
                                                          subject_identifier=lis_source.patient.subject_identifier)
                    self._add_or_remove_warning(lis_source, target, target_identifier_name, warning)
        return value

    def _add_or_remove_warning(self, lis_source, target, target_identifier_name, warning=None):
        """ Logs an error message or removes a previously logged message.

        Previous message is deleted if warning is None."""

        if warning:
            LisImportError.objects.create(
                 model_name=target._meta.object_name,
                 identifier=getattr(lis_source, target_identifier_name),
                 subject_identifier=lis_source.patient.subject_identifier,
                 error_message=warning)
            logger.warning('  {0}'.format(warning))
        else:
            LisImportError.objects.filter(identifier=getattr(target, target_identifier_name)).delete()

