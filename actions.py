from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
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
            label = Label(template=zpl_template)
            label.print_label()
    modeladmin.message_user(request, label.message)

print_test_label.short_description = "Print test label to default printer "


def print_requisition_label(modeladmin, request, queryset):
    label_printer=LabelPrinter()
    if not modeladmin.label_template_name:
        raise ImproperlyConfigured('{0} attribute \'label_template_name\' must be set. '
                                   'Got None.'.format(unicode(modeladmin.__class__.__name__)))
    n = 0
    for requisition in queryset:
        if requisition.is_receive:
            requisition.print_label(requisition=requisition,
                                    remote_addr=request.META.get('REMOTE_ADDR'),
                                    template=modeladmin.label_template_name,
                                    label_count=n,
                                    )
            n += 1
        else:
            messages.add_message(request, messages.ERROR,
                                 'Requisition {0} has not been received. Labels '
                                 'cannot be printed until the specimen is '
                                 'received.'.format(requisition.requisition_identifier,))
    #messages.add_message(request, messages.SUCCESS,
    #                         '{0} label(s) have been printed to {1}'.format(n, cups_server_ip,))
print_requisition_label.short_description = "LABEL: print label"
