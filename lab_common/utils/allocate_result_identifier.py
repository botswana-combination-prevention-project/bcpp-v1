from lab_order.models import Order
from lab_result.models import Result


def get_identifier(order): 
    cnt = Result.objects.filter(order=order,).count()
    cnt += 1
    if cnt < 10:
        pad = '0'
    else:
        pad = ''
    return '%s-%s%s' % (order.order_identifier, pad, cnt)

