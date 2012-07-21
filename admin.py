from django.contrib import admin
from bhp_common.models import MyModelAdmin
from lab_barcode.models import ZplTemplate, LabelPrinter, Client, TestLabel
from forms import ZplTemplateForm, LabelPrinterForm
from actions import print_test_label
from classes import ModelLabel


class ZplTemplateAdmin(MyModelAdmin):

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


class ClientAdmin(MyModelAdmin):

    list_display = (
        "name",
        "ip",
        "label_printer",
    )

admin.site.register(Client, ClientAdmin)


class ClientInline(admin.TabularInline):

    model = Client
    extras = 3


class LabelPrinterAdmin(MyModelAdmin):

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


class TestLabelAdmin(MyModelAdmin):

    list_display = ('identifier', 'user_created', 'created')
    actions = [print_test_label, ]
    list_per_page = 25
    label_template_name = 'laboratory'

    def save_model(self, request, obj, form, change):
        model_label_printer = ModelLabel()
        model_label_printer.print_label_on_save_model(request, obj)
        super(TestLabelAdmin, self).save_model(request, obj, form, change)

admin.site.register(TestLabel, TestLabelAdmin)
