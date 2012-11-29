from django.contrib import admin
#from django.db.models import ForeignKey
#from django.core.urlresolvers import reverse
#from bhp_lab_entry.models import ScheduledLabEntryBucket
from bhp_visit_tracking.classes import BaseVisitTrackingModelAdmin
#from lab_clinic_api.models import Panel
from lab_panel.models import Panel
from lab_requisition.actions import flag_as_received, flag_as_not_received, flag_as_not_labelled
from lab_requisition.actions import print_requisition_label


class BaseRequisitionModelAdmin(BaseVisitTrackingModelAdmin):

    actions = [flag_as_received,
               flag_as_not_received,
               flag_as_not_labelled,
               print_requisition_label, ]

    def __init__(self, *args, **kwargs):
        super(BaseRequisitionModelAdmin, self).__init__(*args, **kwargs)
        self.fields = [
            self.visit_fieldname,
            "requisition_datetime",
            "is_drawn",
            "reason_not_drawn",
            "drawn_datetime",
            "site",
            "panel",
            "test_code",
            "aliquot_type",
            "item_type",
            "item_count_total",
            "estimated_volume",
            "priority",
            "comments", ]
        self.radio_fields = {
            "is_drawn": admin.VERTICAL,
            "reason_not_drawn": admin.VERTICAL,
            "item_type": admin.VERTICAL,
            "priority": admin.VERTICAL,
            "site": admin.VERTICAL,
            }
        self.list_display = [
            'requisition_identifier',
            'specimen_identifier',
            'subject',
            'visit',
            "requisition_datetime",
            "panel",
            'hostname_created',
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed',
            'is_lis',
            'is_receive_datetime',
            'is_labelled_datetime', ]
        self.list_filter = [
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed',
            'is_lis',
            "requisition_datetime",
            'is_receive_datetime',
            'is_labelled_datetime',
            'hostname_created', ]
        self.search_fields = [
            '{0}__appointment__registered_subject__subject_identifier'.format(self.visit_fieldname,),
            'specimen_identifier',
            'requisition_identifier']
        self.filter_horizontal = ["test_code", ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                               request,
                                                                               **kwargs)

#    def save_model(self, request, obj, form, change):
#        if not self.visit_model:
#            raise AttributeError('visit_model cannot be None. Specify in the ModelAdmin '
#                                 ' class. e.g. visit_model = \'maternal_visit\'')
#
#        ScheduledLabEntryBucket.objects.update_status(
#            model_instance=obj,
#            visit_model=self.visit_model,
#            )
#        return super(BaseRequisitionModelAdmin, self).save_model(request, obj, form, change)
#
#    def delete_model(self, request, obj):
#
#        if not self.visit_model:
#            raise AttributeError('delete_model(): visit_model cannot be None. '
#                                 'Specify in the ModelAdmin class. '
#                                 'e.g. visit_model = \'maternal_visit\'')
#        ScheduledLabEntryBucket.objects.update_status(
#            model_instance=obj,
#            visit_model=self.visit_model,
#            action='delete',
#            )
#        return super(BaseRequisitionModelAdmin, self).delete_model(request, obj)

#    def delete_view(self, request, object_id, extra_context=None):
#
#        """ Tries to redirect if enough information is available in the admin model."""
#
#        if not self.visit_model:
#            raise AttributeError('visit_model cannot be None. Specify in the ModelAdmin class. '
#                                 'e.g. visit_model = \'maternal_visit\'')
#        if not self.dashboard_type:
#            raise AttributeError('dashboard_type cannot be None. Specify in the ModelAdmin '
#                                 'class. e.g. dashboard_type = \'subject\'')
#            self.dashboard_type = 'subject'
#        visit_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name][0].name
#        pk = self.model.objects.values(visit_fk_name).get(pk=object_id)
#        visit_instance = self.visit_model.objects.get(pk=pk[visit_fk_name])
#        subject_identifier = visit_instance.appointment.registered_subject.subject_identifier
#        visit_code = visit_instance.appointment.visit_definition.code
#        result = super(BaseRequisitionModelAdmin, self).delete_view(request, object_id, extra_context)
#        result['Location'] = reverse('dashboard_visit_url', kwargs={'dashboard_type': self.dashboard_type,
#                                                                     'subject_identifier': subject_identifier,
#                                                                     'appointment': visit_instance.appointment.pk,
#                                                                     'visit_code': unicode(visit_code)})
#        return result