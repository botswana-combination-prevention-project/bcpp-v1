from datetime import datetime
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lab_result.models import Result
from lab_result_item.models import ResultItem


@dajaxice_register
def print_result_report(request, result_identifier):

    dajax = Dajax()

    if result_identifier is not None:

        oResult = Result.objects.using('lab_api').get(result_identifier__exact=result_identifier)
        oResultItems = ResultItem.objects.using('lab_api').filter(result=oResult)
        
        context = {
        'result': oResult,
        'receive': oResult.order.aliquot.receive,
        'order': oResult.order,
        'aliquot': oResult.order.aliquot,
        'result_items': oResultItems,
        'result_include_file': "detail.html",
        'receiving_include_file':"receiving.html",
        'orders_include_file': "orders.html",
        'result_items_include_file': "result_items.html",
        'top_result_include_file': "result_include.html",
        }


    rendered = render_to_string('result_report_single.html', { 'result_report': context })

    dajax.assign('#result_report','innerHTML',rendered)

    return dajax.json()
  
