from datetime import datetime
from django.contrib import messages

def flag_as_received(modeladmin, request, queryset, **kwargs):

    """wrap this in your own so that you can pass the kwargs
    
        def my_flag_as_received(modeladmin, request, queryset):
            flag_as_received(modeladmin, request, queryset, site_code='20', protocol_code='041')
        my_flag_as_received.short_description = "Flag as received against requisition"
    
    """
            
    site_code = kwargs.get('site_code')
    protocol_code = kwargs.get('protocol_code')        
    for qs in queryset:
        if not qs.specimen_identifier:
            qs.specimen_identifier = qs.__class__.objects.get_identifier(site_code=site_code, protocol_code=protocol_code)
            qs.is_receive = True
            qs.is_receive_datetime = datetime.today()
            qs.save()
            
#flag_as_received.short_description = "Flag as received against requisition"

def flag_as_not_received(modeladmin, request, queryset):

    for qs in queryset:
        #if not qs.specimen_identifier:
        qs.specimen_identifier=None
        qs.is_receive = False
        qs.is_receive_datetime = datetime.today()
        qs.save()
            
flag_as_not_received.short_description = "UNFLAG: flag as NOT received"


def flag_as_not_labelled(modeladmin, request, queryset):
    for qs in queryset:
        #if not qs.specimen_identifier:
        qs.is_labelled = False
        qs.save()

flag_as_not_labelled.short_description = "UNLABEL: flag as NOT labelled"


def print_barcode_labels(modeladmin, request, queryset):
    #TODO: remote_addr='127.0.0.1'
    n = 0
    for requisition in queryset:
        if requisition.is_receive:
            requisition.__class__.objects.print_label(requisition=requisition,remote_addr='127.0.0.1')    
            requisition.is_labelled = True
            requisition.is_labelled_datetime = datetime.today()             
            requisition.save()
            n += 1       
        else:
            messages.add_message(request, messages.ERROR, 'Requisition %s has not been received. Labels cannot be printed until the specimen is received.' % (requisition.requisition_identifier,))
            #break            
    messages.add_message(request, messages.SUCCESS, '%s labels have been printed' % (n,))                        
        
print_barcode_labels.short_description = "LABEL: print label"
    

