import re
import logging
import pyodbc

from django.conf import settings
from django.db.models import get_model

from lab_order.models import Order as LisOrder
from lab_result.models import Result as LisResult
#from lab_result_item.models import ResultItem as LisResultItem


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class DmisTools(object):

    def __init__(self):
        self.lab_db = 'lab_api'
        self.dmis_data_source = settings.LAB_IMPORT_DMIS_DATA_SOURCE

    def unvalidate_on_dmis(self, db, receive_identifier, batch_id, resultset_id):
        """Unvalidates a result on the DMIS for L23 path (use carefully).

        Additionally:
            * deletes any results in LAB21 for this receive_identifier. This might be problematic
              if result spans more than one LAB21/LAB21D record set.
            * deletes all orders on this receive identifier on django-lis
            * deletes all orders for this receive identifier on EDC
        """
        cnxn = pyodbc.connect(self.dmis_data_source)
        cursor = self.cnxn.cursor()
        Order = get_model('lab_clinic_api', 'order')
        if not re.match('[A-Z]{2}[0-9]{5}', receive_identifier):
            raise TypeError('Invalid receive_identifier format. Must be format AA99999.Got {0}'.format(receive_identifier))
        if not re.match('\d+', batch_id):
            raise TypeError('Invalid batch_id format. Must be format an integer. Got {0}'.format(batch_id))
        if not re.match('\d+', resultset_id):
            raise TypeError('Invalid resultset_id format. Must be format an integer. Got {0}'.format(resultset_id))
        logger.info('Unvalidating...')
        sql = ('SELECT l23d.id FROM lab23response as l23 '
               'LEFT JOIN lab23responseq001x0 AS l23d ON l23.q001x0=l23d.qid1x0 '
               'WHERE batchid={batch_id} '
               'AND l23.pid={resultset_id} '
               'AND l23d.bhhrl_ref=\'{receive_identifier}\' '.format(receive_identifier=receive_identifier, batch_id=batch_id, resultset_id=resultset_id))
        l23_id = self.cursor.execute(str(sql)).fetchone()
        if not l23_id:
            logger.error('Invalid criteria. Cannot find validation information in L23 with this criteria.\n')
        else:
            logger.info('    l23 id is {l23_id}'.format(l23_id=l23_id[0]))
            sql = ('DELETE FROM lab21response WHERE pid=\'{receive_identifier}\' '.format(receive_identifier=receive_identifier))
            cursor.execute(str(sql))
            logger.info('    deleted results in L21 for {receive_identifier}'.format(receive_identifier=receive_identifier))
            sql = ('UPDATE lab23responseq001x0 '
                   'SET datesent=convert(datetime,\'09/09/9999\',103), result_accepted=-9 '
                   'WHERE id={l23_id}'.format(l23_id=l23_id[0]))
            cursor.execute(str(sql))
            logger.info('    reset validation in L23 for id = {l23_id}'.format(l23_id=l23_id[0]))
            cnxn.commit()
            # delete on django_lis
            for lis_order in LisOrder.objects.using('lab_api').filter(aliquot__receive__receive_identifier=receive_identifier):
                logger.info('    deleted order on DJANGO-LIS for {0}. Order pk={1}.'.format(receive_identifier, lis_order.pk))
                lis_order.delete()
            # delete on EDC
            # TODO: should this be the order identifier and not receive_identifier?
            for order in Order.objects.filter(aliquot__receive__receive_identifier=receive_identifier):
                logger.info('    deleted order on EDC for {0}. Order pk={1}.'.format(receive_identifier, order.pk))
                order.delete()
            # flag for reimport
            self.flag_for_reimport(receive_identifier)
            logger.info('Done. Validated results have been deleted and validation information reset on the DMIS for :\n'
                        '    batch: {batch_id}\n'
                        '    result set: {resultset_id}\n'
                        '    identifier: {receive_identifier}\n'
                        'You now need to re-validate the result on the DMIS and wait for the DMIS to send the result to LAB21 (10-15min).\n'
                        'Once the result is flagged as sent on the validation page, '
                        're-run import_dmis --import.'.format(receive_identifier=receive_identifier, batch_id=batch_id, resultset_id=resultset_id))
        return True

    def flag_for_reimport(self, receive_identifier):
        """Flags items to be re-imported by changing the modification datetime on the DMIS receiving record."""
        try:
            cnxn = pyodbc.connect(self.dmis_data_source)
        except:
            cnxn = None
        if not cnxn:
            logger.warning('Unable to contact DMIS')
            return None
        cursor = cnxn.cursor()
        sql = ('UPDATE lab01response SET datelastmodified=getdate() WHERE pid=\'{receive_identifier}\''.format(receive_identifier=receive_identifier))
        cursor.execute(str(sql))
        cnxn.commit()
        logger.info('    touched receive record to trigger re-import to django-lis')

    def clear_orphaned_result(self, item=None):
        """Verifies and, if required, deletes the result of a 'PENDING' order on the EDC that has no result items and the result is NEW.

            Args:
                item: can be either a Result instance or an order_identifier.
        """
        Result = get_model('lab_clinic_api', 'result')
        LisResultItem = get_model('lab_result_item', 'resultitem')
        if isinstance(item, Result):
            result = item
        elif Result.objects.filter(order__order_identifier=item).exists():
            result = Result.objects.get(order__order_identifier=item, status='NEW')
        else:
            result = None
        if result:
            # result is on EDC
            # is it on the django-lis?
            if not LisResult.objects.using('lab_api').filter(result_identifier=result.result_identifier).exists():
                lis_result = LisResult.objects.using('lab_api').get(result_identifier=result.result_identifier)
                # ...with resultitems?
                if not LisResultItem.objects.using('lab_api').filter(result=lis_result).exists():
                    lis_order = lis_result.order
                    lis_order.status = 'WITHDRAWN'
                    logger.info('    refreshing order status on django-lis for order {0}'.format(lis_order.order_identifier))
                    lis_order.save()
                    logger.info('    deleting orphaned result on django-lis (no items) for order {0}'.format(lis_result.order.order_identifier))
                    lis_result.delete()
            # does it have resultitems on the EDC?
            ResultItem = get_model('lab_clinic_api', 'resultitem')
            if not ResultItem.objects.filter(result=result).exists():
                order = result.order
                logger.info('    refreshing order status on EDC for order {0}'.format(order.order_identifier))
                order.save()
                logger.info('    deleting orphaned result (no items) on EDC for order {0}'.format(result.order.order_identifier))
                result.delete()

    def flag_withdrawn_order(self, order, save=True):
        """Deletes an order if it no longer exists on the DMIS and does not have a result on file.

        Only try for order identifiers that are the id from lab21.id. In some cases the order identifier
        is the PID of lab01response when received only on the LIS.

        .. note:: Order identifier is LAB21.id in almost all cases except for samples received only.
        """
        try:
            cnxn = pyodbc.connect(self.dmis_data_source)
        except:
            cnxn = None
        if not cnxn:
            logger.warning('Unable to contact DMIS')
            return None
        cursor = cnxn.cursor()
        order_status = None
        # make sure the order identifier is an integer
        sql_template = 'select id from lab21response where id={0}'
        if not re.match('^\d+$', order.order_identifier):
            # if not an integer, query against PID instead of ID
            logger.info('    INVALID order identifier {0}'.format(order.order_identifier))
            #if re.match('^\w+$', order.order_identifier):
            #    sql_template = 'select id from lab21response where pid=\'{0}\''
        # query DMIS for this LAB21.id
        sql = (sql_template).format(order.order_identifier)
        lab21_id = cursor.execute(str(sql)).fetchone()
        if not lab21_id:
            # does not exist on the DMIS. prepare to flag as withdrawn on django-lis and EDC
            order_status = 'WITHDRAWN'
            if LisOrder.objects.using('lab_api').filter(order_identifier=order.order_identifier).exists():
                lis_order = LisOrder.objects.using('lab_api').get(order_identifier=order.order_identifier)
                lis_order.status = order_status
                if save:
                    logger.info('    changing order {0} to WITHDRAWN on django-lis.'.format(order.order_identifier))
                    lis_order.save(using='lab_api')
            if save:
                # only save if you are not in Order.save()
                order.status = order_status
                logger.info('    changing order {0} to WITHDRAWN on edc.'.format(order.order_identifier))
                order.save()
        return order_status

    def is_withdrawn_order(self, order):
        """Wraps :mod:`flag_withdrawn_order` to return True/False.

        Called by Order :func:save()."""
        if self.flag_withdrawn_order(order, False):
            return True
        else:
            return False
