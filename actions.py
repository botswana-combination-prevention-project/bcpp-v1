import subprocess, re
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
