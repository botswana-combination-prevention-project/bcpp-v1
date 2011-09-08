from lab_order.models import Order
from lab_result.models import Result


def AllocateResultIdentifier(oOrder): 

    cnt = Result.objects.filter(order=oOrder,).count()
    
    cnt += 1
    
    if cnt < 10:
        pad = '0'
    else:
        pad = ''    
    
    return '%s-%s%s' % (oOrder.order_identifier, pad, cnt)

