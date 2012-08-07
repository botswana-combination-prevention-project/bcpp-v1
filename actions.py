from datetime import datetime

from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages

from lab_barcode.exceptions import PrinterException


def flag_as_received(modeladmin, request, queryset, **kwargs):
    """ flag as received and generate a globally unique identifier.
    Note the model is a SubjectRequisition"""

    for qs in queryset:
        #if not qs.specimen_identifier:
        qs.is_receive = True
        qs.is_receive_datetime = datetime.today()
        qs.save()

flag_as_received.short_description = "RECEIVE as received against requisition"


def flag_as_not_received(modeladmin, request, queryset):

    for qs in queryset:
        qs.is_receive = False
        qs.is_receive_datetime = datetime.today()
        qs.save()
flag_as_not_received.short_description = "UN-RECEIVE: flag as NOT received"


def flag_as_not_labelled(modeladmin, request, queryset):
    for qs in queryset:
        qs.is_labelled = False
        qs.save()

flag_as_not_labelled.short_description = "UN-LABEL: flag as NOT labelled"


def print_requisition_label(modeladmin, request, requisitions):
    #if not modeladmin.label_template:
    #    raise ImproperlyConfigured('{0} attribute \'label_template\' must be set. '
    #                              'Got None.'.format(unicode(modeladmin.__class__.__name__)))
    try:
        for requisition in requisitions:
            if requisition.is_receive:
                requisition.print_label(request)
            else:
                messages.add_message(request, messages.ERROR,
                                     'Requisition {0} has not been received. Labels '
                                     'cannot be printed until the specimen is '
                                     'received.'.format(requisition.requisition_identifier,))
    except PrinterException as e:
        messages.add_message(request, messages.ERROR, e.value)

print_requisition_label.short_description = "LABEL: print requisition label"
