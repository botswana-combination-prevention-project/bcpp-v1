#import subprocess, re
from datetime import datetime
from django.contrib import messages
from lab_barcode.models import LabelPrinter
from lab_barcode.classes import Label

def print_test_label(modeladmin, request, queryset):

    #get printer
    label_printer = LabelPrinter.objects.filter(default=True)
    
    if label_printer:
        # get default printer, or the first default printer
        label_printer = LabelPrinter.objects.filter(default=True)[0]

        # templates to print
        for zpl_template in queryset:

            label = Label(template = zpl_template)
            
            # remove brackets fromplaceholders
            #template  = re.sub('\{','', zpl_template.template) 
            #template  = re.sub('\}','', template)             
            
            label.print_label()
       
    modeladmin.message_user(request, label.message)
            

print_test_label.short_description = "Print test label to default printer "


def print_barcode_labels(modeladmin, request, queryset):
    #TODO: remote_addr='127.0.0.1'
    n = 0
    
    remote_addr = request.META.get('REMOTE_ADDR')
    if not LabelPrinter.objects.filter(client__ip=remote_addr) and not remote_addr=='127.0.0.1':
        #cups_server_ip = LabelPrinter.objects.get(client__ip=remote_addr).cups_server_ip
        #else:
        messages.add_message(request, messages.ERROR, 'The client %s is not configured to print. See lab_barcode app: label_printer model.' % (remote_addr,))
 
    
    for requisition in queryset:
        if requisition.is_receive:
            requisition.__class__.objects.print_label(requisition=requisition,remote_addr=remote_addr)    
            #requisition.is_labelled = True
            #requisition.is_labelled_datetime = datetime.today()             
            #requisition.save()
            n += 1       
        else:
            messages.add_message(request, messages.ERROR, 'Requisition %s has not been received. Labels cannot be printed until the specimen is received.' % (requisition.requisition_identifier,))
            #break            
    messages.add_message(request, messages.SUCCESS, '%s labels have been printed' % (n,))                        
        
print_barcode_labels.short_description = "LABEL: print label"
    