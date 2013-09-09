from base_packing_list_model_admin import BasePackingListModelAdmin


class BasePackingListAdmin(BasePackingListModelAdmin):

    def save_model(self, request, obj, form, change):

        if not change:
            obj.user_created = request.user
        else:
            obj.user_modified = request.user

        super(BasePackingListAdmin, self).save_model(request, obj, form, change)

        lst = filter(None, obj.list_items.replace('\r', '').split('\n'))

        for item in lst:
            if item:
                if not isinstance(self.requisition, list):
                    self.requisition = [self.requisition, ]
                for requisition in self.requisition:
                    if requisition.objects.filter(specimen_identifier=item):
                        subject_requisition = requisition.objects.get(specimen_identifier=item)
                        if self.packing_list_item_model.objects.filter(packing_list=obj,
                                                                       item_reference=subject_requisition.specimen_identifier):
                            packing_list_item = self.packing_list_item_model.objects.get(packing_list=obj,
                                                                                         item_reference=subject_requisition.specimen_identifier)
                            packing_list_item.item_description = '{subject_identifier} ({initials}) VISIT:{visit} DOB:{dob}'.format(
                                                                                     subject_identifier=subject_requisition.get_visit().appointment.registered_subject.subject_identifier,
                                                                                     initials=subject_requisition.get_visit().appointment.registered_subject.initials,
                                                                                     visit=subject_requisition.get_visit().appointment.visit_definition.code,
                                                                                     dob=subject_requisition.get_visit().appointment.registered_subject.dob,)
                            packing_list_item.requisition = subject_requisition._meta.object_name.lower()
                            packing_list_item.panel = subject_requisition.panel
                            packing_list_item.item_priority = subject_requisition.priority
                            packing_list_item.user_modified = request.user
                            packing_list_item.save()
                            subject_requisition.is_packed = True
                            subject_requisition.save()
                        else:

                            self.packing_list_item_model.objects.create(
                                packing_list=obj,
                                item_reference=subject_requisition.specimen_identifier,
                                requisition=subject_requisition._meta.object_name.lower(),
                                item_description='{subject_identifier} ({initials}) VISIT:{visit} DOB:{dob}'.format(
                                                         subject_identifier=subject_requisition.get_visit().appointment.registered_subject.subject_identifier,
                                                         initials=subject_requisition.get_visit().appointment.registered_subject.initials,
                                                         visit=subject_requisition.get_visit().appointment.visit_definition.code,
                                                         dob=subject_requisition.get_visit().appointment.registered_subject.dob,),
                                panel=subject_requisition.panel,
                                item_priority=subject_requisition.priority,
                                user_created=request.user,
                                )
                            subject_requisition.is_packed = True
                            subject_requisition.save()
