from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyTabularInline
from lab_packing.classes import BasePackingListModelAdmin
from lab_packing.forms import *
from lab_packing.models import *


"""
In models define a proxy model packing list for each requisition model, like this

    from django.db import models
    from audit_trail.audit import AuditTrail
    from lab_packing.models import PackingList


    class InfantPackingList(PackingList):
        
        history = AuditTrail()

        class Meta:
            proxy = True
            app_label = "tshipidi_lab"
            verbose_name = 'Infant Packing List' 


in the local xxxx_lab app add something like this to admin
for each packing list / requisition model defined in models. 


    from lab_packing.admin import PackingListAdmin

    class InfantPackingListAdmin(PackingListAdmin): 

        form = InfantPackingListForm
        requisition = InfantRequisition
        
    admin.site.register(InfantPackingList, InfantPackingListAdmin)

"""
    
class PackingListAdmin(BasePackingListModelAdmin): 
    
    form = PackingListForm    
    
    def save_model(self, request, obj, form, change):
        
        if not change:
            obj.user_created = request.user
        else:
            obj.user_modeified = request.user        
        
        super(PackingListAdmin, self).save_model(request, obj, form, change)

        lst = obj.list_items.replace('\r', '').split('\n')
        
        for item in lst:
            if item:
                subject_requisition = self.requisition.objects.get(specimen_identifier=item)
                if PackingListItem.objects.filter(packing_list=obj, item_reference=subject_requisition.specimen_identifier):
                    packing_list_item = PackingListItem.objects.get(packing_list=obj, item_reference=subject_requisition.specimen_identifier)
                    packing_list_item.item_description = '%s (%s) DOB:%s' % (subject_requisition.subject_visit.appointment.registered_subject.subject_identifier, subject_requisition.subject_visit.appointment.registered_subject.initials, subject_requisition.subject_visit.appointment.registered_subject.dob,)
                    packing_list_item.user_modified = request.user
                    packing_list_item.save()                    
                    subject_requisition.is_packed = True
                    
                    subject_requisition.save()                    
                else:
                    PackingListItem.objects.create(
                        packing_list=obj,
                        item_reference = subject_requisition.specimen_identifier,
                        item_description = '%s (%s) DOB:%s' % (subject_requisition.subject_visit.appointment.registered_subject.subject_identifier, subject_requisition.subject_visit.appointment.registered_subject.initials, subject_requisition.subject_visit.appointment.registered_subject.dob,),
                        user_created = request.user,                        
                        )
                    subject_requisition.is_packed = True
                    subject_requisition.save()
                    
        
    
admin.site.register(PackingList, PackingListAdmin)


class PackingListItemAdmin(MyModelAdmin):

    search_fields = ('packing_list__pk','item_description','item_reference',)
    list_display = ('packing_list','item_reference','item_description', 'created', 'user_created')
    list_filter = ('created',)
    
    def delete_model(self, request, obj):
    
        if self.requisition.objects.filter(specimen_identifier=obj.item_reference):
            subject_requisition = self.requisition.objects.get(specimen_identifier=obj.item_reference)                            
            subject_requisition.is_packed = False
            subject_requisition.save()
        
        super(PackingListItemAdmin, self).delete_model(request, obj)
   
admin.site.register(PackingListItem, PackingListItemAdmin)

