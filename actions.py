from datetime import datetime

def flag_as_received(modeladmin, request, queryset, **kwargs):
    """ flag as received and generate a globally unique identifier.
    Note the model is a SubjectRequisition"""
    
    for qs in queryset: 
        if not qs.specimen_identifier:
            qs.specimen_identifier = qs.__class__.objects.get_global_identifier(site_code = qs.site.site_code, 
                                                                                protocol_code = qs.protocol)
            qs.is_receive = True
            qs.is_receive_datetime = datetime.today()
            qs.save()
            
flag_as_received.short_description = "Flag as received against requisition"

def flag_as_not_received(modeladmin, request, queryset):

    for qs in queryset:
        qs.specimen_identifier = None
        qs.is_receive = False
        qs.is_receive_datetime = datetime.today()
        qs.save()
            
flag_as_not_received.short_description = "UNFLAG: flag as NOT received"


def flag_as_not_labelled(modeladmin, request, queryset):
    for qs in queryset:
        qs.is_labelled = False
        qs.save()

flag_as_not_labelled.short_description = "UNLABEL: flag as NOT labelled"




