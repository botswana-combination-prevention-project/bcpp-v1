import cStringIO as StringIO
import ho.pisa as pisa
import cgi
from math import ceil,trunc
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template import Context
from django import http
from bhp_lab_core.models import Result, ResultItem


@login_required
def view_result_as_pdf(request, **kwargs):

    section_name = kwargs.get('section_name')
    search_name = "result"
    result_identifier = kwargs.get('result_identifier')
    limit = 20
    template = 'result_report_pdf.html'
                  
    result = get_object_or_404(Result, result_identifier=result_identifier)
    items = ResultItem.objects.filter(result=result)
    
    total_page_number = trunc(ceil(items.count()/float(18)))
    
    #raise TypeError(items.count()/float(18))
    
    payload = {
        'pagesize': 'A4',
        'total_page_number':total_page_number,
        'result': result,
        'receive': result.order.aliquot.receive,
        'order': result.order,
        'aliquot': result.order.aliquot,
        'result_items': items,
        'section_name': section_name,
        'result_include_file': "detail.html",
        'receiving_include_file':"receiving.html",
        'orders_include_file': "orders.html",
        'result_items_include_file': "result_items.html",
        'top_result_include_file': "result_include.html",
    }
    
    file_data = render_to_string(template, payload, RequestContext(request))
    myfile = StringIO.StringIO()
    pisa.CreatePDF(file_data, myfile)
    myfile.seek(0)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(myfile.getvalue(),mimetype='application/pdf')
    response['Content-Disposition'] = "attachment; filename=%s.pdf" % (result.result_identifier)
    return response
    

