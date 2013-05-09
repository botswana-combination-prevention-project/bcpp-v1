from bhp_base_admin.admin import BaseModelAdmin


class BasePackingListItemAdmin(BaseModelAdmin):

    search_fields = ('packing_list__pk', 'packing_list__timestamp', 'item_description', 'item_reference',)
    list_display = ('specimen', 'priority', 'panel', 'description', 'gender', 'drawn_datetime', 'clinician', 'view_packing_list',)
    list_filter = ('created', 'panel')

    def delete_model(self, request, obj):

        if not isinstance(self.subject_requisition, list):
            self.subject_requisition = [self.subject_requisition, ]
        for requisition in self.requisition:
            if requisition.objects.filter(specimen_identifier=obj.item_reference):
                subject_requisition = requisition.objects.get(specimen_identifier=obj.item_reference)
                subject_requisition.is_packed = False
                subject_requisition.save()
        super(BasePackingListItemAdmin, self).delete_model(request, obj)
