import random
import datetime
from django.http import HttpResponse
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from matplotlib.dates import DateFormatter
from lab_clinic_api.models import ResultItem

"""http://localhost:8000/mpepu/specimens/charts/simple.png"""

def longitudinal_result(request, **kwargs):

    return ''
    """
    subject_identifier = kwargs.get('subject_identifier')
    test_code = []
    if kwargs.get('test_code') == 'VL':
        test_code = []
        test_code.append('auvl')
        test_code.append('phm')        
        test_code.append('phs')        
    else:
        test_code.append(kwargs.get('test_code'))
    fig=Figure()
    fig.set_label(test_code)
    ax=fig.add_subplot(111, title=kwargs.get('test_code'))
    ax.set_xlabel('time')

       
    x=[]
    y=[]
    now=datetime.datetime.now()
    result_items = ResultItem.objects.filter(result__lab__subject_identifier=subject_identifier, test_code__code__in=test_code)
    test_codes = [result_item.test_code.code for result_item in result_items]
    ax.set_ylabel('&'.join(list(set(test_codes))))
    
    x = [result_item.result_item_datetime for result_item in result_items]
    y = [result_item.result_item_value for result_item in result_items]
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response
    """
