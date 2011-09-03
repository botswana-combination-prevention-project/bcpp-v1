from django.contrib import admin
from bhp_common.models import MyModelAdmin
from lab_barcode.models import ZplTemplate, LabelPrinter, Client
from forms import ZplTemplateForm, LabelPrinterForm
from actions import print_test_label

# ZplTemplate
class ZplTemplateAdmin(MyModelAdmin): 

    form = ZplTemplateForm
    
    fields = (
        "name",
        "template",
        "default",        
    )

    radio_fields = {
        
    }

    filter_horizontal = (
        
    )

    actions = [print_test_label]

    """"""

admin.site.register(ZplTemplate, ZplTemplateAdmin)

class ClientInline(admin.TabularInline):

    model = Client
    extras =3


# LabelPrinter
class LabelPrinterAdmin(MyModelAdmin): 

    form = LabelPrinterForm

    fields = (
        "cups_printer_name",
        "cups_server_ip",
        "default",
    )

    radio_fields = {
        
    }

    filter_horizontal = (
        
    )

    inlines = [ClientInline,]

    list_display = ('cups_printer_name', 'cups_server_ip', 'default' )

admin.site.register(LabelPrinter, LabelPrinterAdmin)
