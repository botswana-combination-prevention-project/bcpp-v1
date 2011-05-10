def batch_print_result_as_pdf(**kwargs):
    import cStringIO as StringIO
    import ho.pisa as pisa
    import sys, os, subprocess
    from math import ceil,trunc
    from django.template.loader import render_to_string
    from django.shortcuts import get_object_or_404
    from bhp_lab_core.models import Result, ResultItem

    template = 'result_report_pdf.html'
    result_ids = ['1240636-01','1242053-01','1241852-01','1242079-01','1241851-01']
    #result_ids = ['1240636-01','1242053-01']
   
    for result_identifier in result_ids:
        print_result_as_pdf(result_identifier,template)
                
    return 
    
def print_result_as_pdf(result_identifier,template):
    import cStringIO as StringIO
    import ho.pisa as pisa
    import sys, os, subprocess
    from math import ceil,trunc
    from django.template.loader import render_to_string
    from django.shortcuts import get_object_or_404
    from bhp_lab_core.models import Result, ResultItem

    section_name = 'result'
    search_name = 'result'
    num_items_last_page = 18
    num_items_first_page = 13
    num_items_per_page = 23
    total_page_number = 1    
    
    result = get_object_or_404(Result, result_identifier=result_identifier)
    
    items = ResultItem.objects.filter(result=result)
    
    num_items = items.count()
    
    if num_items > num_items_first_page:
    
        if (num_items - num_items_first_page) > num_items_last_page:
        
            num_items_other = num_items - num_items_first_page - num_items_last_page
            
            total_page_number += trunc( ceil( num_items_other / float( num_items_per_page ) ) )
            
        else:
        
            total_page_number = 2
   
    if result_identifier is not None:
        file_name = "/home/pmotshegwa/sources/printed_results/%s.pdf" % (result_identifier)
        file = open(file_name, "wb")
         
        result = get_object_or_404(Result, result_identifier=result_identifier)
        items = ResultItem.objects.filter(result=result)
        
        total_page_number = trunc(ceil(items.count()/float(18)))
        
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
        
        file_data = render_to_string(template, payload,)
        myfile = StringIO.StringIO()
        pdf = pisa.CreatePDF(file_data, myfile)
              
        if pdf.err:
             print "*** %d ERRORS OCCURED" % pdf.err
        else:
        
            # Write pdf file to disk
            file.write(myfile.getvalue())
            file.close()
            command = "lp {0}".format( file_name )

            try:
                p = subprocess.Popen(command, shell = True)
                pid , sts = os.waitpid(p.pid, 0)
            except subprocess.CalledProcessError, e:
                print "Error", e.returncode
                print e.output
                
    return 
    
