from django.contrib import admin
from django.contrib import messages

from bhp_base_admin.admin import BaseModelAdmin
from lab_barcode.models import ZplTemplate, LabelPrinter, Client, TestLabel
from forms import ZplTemplateForm, LabelPrinterForm
from lab_barcode.exceptions import PrinterException
from actions import print_test_label
from classes import ModelLabel


class ZplTemplateAdmin(BaseModelAdmin):

    form = ZplTemplateForm

    fields = (
        "name",
        "template",
        "default",
    )

    list_display = ('name', 'default',)
    radio_fields = {}
    filter_horizontal = ()
    actions = [print_test_label]

admin.site.register(ZplTemplate, ZplTemplateAdmin)


class ClientAdmin(BaseModelAdmin):

    list_display = (
        "name",
        "ip",
        "label_printer",
    )

admin.site.register(Client, ClientAdmin)


class ClientInline(admin.TabularInline):

    model = Client
    extras = 3


class LabelPrinterAdmin(BaseModelAdmin):

    form = LabelPrinterForm

    fields = (
        "cups_printer_name",
        "cups_server_ip",
        "default",
    )

    radio_fields = {}
    filter_horizontal = ()
    inlines = [ClientInline, ]
    list_display = ('cups_printer_name', 'cups_server_ip', 'default')

admin.site.register(LabelPrinter, LabelPrinterAdmin)


class TestLabelAdmin(BaseModelAdmin):

    list_display = ('identifier', 'user_created', 'created')
    actions = [print_test_label, ]
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        model_label = ModelLabel()
        try:
            model_label.print_label(request, obj, obj.copies, obj.identifier)
        except PrinterException as e:
            messages.add_message(request, messages.ERROR, e.value)
        super(TestLabelAdmin, self).save_model(request, obj, form, change)

admin.site.register(TestLabel, TestLabelAdmin)
