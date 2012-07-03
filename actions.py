from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from lab_barcode.models import LabelPrinter
from lab_barcode.classes import Label

def print_test_label(modeladmin, request, queryset):

    #get printer
    label_printer = LabelPrinter.objects.filter(default=True)
    if label_printer:
        # get default printer, or the first default printer
        label_printer=LabelPrinter.objects.filter(default=True)[0]
        # templates to print
        for zpl_template in queryset:
            label=Label(template = zpl_template)
            
            # remove brackets fromplaceholders
            #template  = re.sub('\{','', zpl_template.template) 
            #template  = re.sub('\}','', template)             
            
            label.print_label()
    modeladmin.message_user(request, label.message)

print_test_label.short_description = "Print test label to default printer "


def print_barcode_labels(modeladmin, request, queryset):
    #use the remote addr to determine which cups_server_ip to select
    remote_addr = request.META.get('REMOTE_ADDR')
    if not modeladmin.label_template_name:
        raise ImproperlyConfigured('{0} attribute \'label_template_name\' must be set. Got None.'.format(unicode(modeladmin.__class__.__name__)))
    template_name = modeladmin.label_template_name
    if not LabelPrinter.objects.filter(client__ip=remote_addr):
        messages.add_message(request, messages.ERROR, 'The client %s is not configured for any printer. See lab_barcode app: label_printer model.' % (remote_addr,))
    else:
        if LabelPrinter.objects.filter(client__ip=remote_addr).count() > 1:
            messages.add_message(request, messages.ERROR, 'The client %s is configured for more than one printer. See lab_barcode app: label_printer model.' % (remote_addr,))
        else:    
            cups_server_ip=LabelPrinter.objects.get(client__ip=remote_addr).cups_server_ip
            n=0
            for requisition in queryset:
                if requisition.is_receive:
                    requisition.print_label(requisition = requisition,
                                            cups_server_ip = cups_server_ip,
                                            template_name=template_name,
                                            )
                    n += 1       
                else:
                    messages.add_message(request, messages.ERROR, 'Requisition %s has not been received. Labels cannot be printed until the specimen is received.' % (requisition.requisition_identifier,))
                    #break            
            messages.add_message(request, messages.SUCCESS, '%s label(s) have been printed to %s' % (n,cups_server_ip,))                        
        
print_barcode_labels.short_description = "LABEL: print label"
    