import logging
import pyodbc
import re
from django.conf import settings
from django.core.management.base import BaseCommand
from lab_clinic_api.models import Order, Result, ResultItem
from lab_order.models import Order as DmisOrder


class Command(BaseCommand):

    args = ()
    help = 'Clear orphan orders that no longer exist on the DMIS from django-lis and EDC.'

    def handle(self, *args, **options):
        # clear orphaned results
        # if a result exists with no result items it should not exist, so delete it
        tot = Result.objects.filter(status='NEW').count()
        for n, result in enumerate(Result.objects.filter(status='NEW')):
            print '{0} / {1} Result for order {2}'.format(n, tot, result.order.order_identifier)
            if not ResultItem.objects.filter(result=result).exists():
                print '    deleting result (no items) for order {0}'.format(result.order.order_identifier)
                order = result.order
                result.delete()
                # force order status to update to pending
                order.save()
        #if an order is pending, confirm that the order id still exists on the DMIS
        # if not, delete it from both the django-lis and the EDC
        # note that order_identifer = lab21.id
        dmis_data_source = settings.LAB_IMPORT_DMIS_DATA_SOURCE
        cnxn2 = pyodbc.connect(dmis_data_source)
        cursor = cnxn2.cursor()
        tot = Order.objects.filter(status='PENDING').count()
        invalid_identifiers = []
        for n, order in enumerate(Order.objects.filter(status='PENDING')):
            print ('{0} / {1} Order {2} {3}'.format(n, tot, order.order_identifier, order.aliquot.receive.receive_identifier))
            if not re.match('\d+', order.order_identifier):
                print '    invalid order identifier {0}'.format(order.order_identifier)
                invalid_identifiers.append(order.order_identifier)
            else:
                sql = ('select id from lab21response where id={0}').format(order.order_identifier)
                lab21_id = cursor.execute(str(sql)).fetchone()
                if lab21_id:
                    print lab21_id
                    # see if the same specimen identifier has a result on EDC
                    # if so, delete this order on the EDC, it has been filled
                    # using another order
                    if ResultItem.objects.filter(result__order__aliquot__receive__receive_identifier=order.aliquot.receive.receive_identifier).exists():
                        print '    result items exists'
                        if DmisOrder.objects.using('lab_api').filter(order_identifier__in=lab21_id):
                            print ('    deleting from django-lis')
                            # DmisOrder.objects.using('lab_api').get(order__order_identifier=order.order_identifier).delete()
                            print ('    deleting from edc')
                            # order.delete()
                else:
                    # does not exist on the DMIS. 
                    # is there a complete order for this same receive identifier?
                    if ResultItem.objects.filter(result__order__aliquot__receive__receive_identifier=order.aliquot.receive.receive_identifier).exists():
                        for ord in Order.objects.filter(aliquot__receive__receive_identifier=order.aliquot.receive.receive_identifier, status='COMPLETE'):
                            print ('    complete order on file, deleting pending order. See {0}'.format(ord))
                            print ('    deleting from django-lis')
                            DmisOrder.objects.using('lab_api').get(order__order_identifier=order.order_identifier).delete()
                            print ('    deleting from edc')
                            order.delete()
        #print ' ,'.join(invalid_identifiers)
