#from datetime import datetime
from django.core.urlresolvers import reverse
from django.db.models import get_model
from bhp_base_admin.admin import BaseModelAdmin


class BaseAppointmentModelAdmin(BaseModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to 'appointment', such as your visit model(s).

    In the child ModelAdmin class set the following attributes, for example::

        visit_model_foreign_key = 'maternal_visit'
        dashboard_type = 'maternal'

    if you are tracking labs, also include a model that inherets from lab_requisition.models.BaseRequisition, e.g.::

        requisition_model = MaternalRequisition

    """
    date_hierarchy = 'report_datetime'

    def __init__(self, *args, **kwargs):
        # dashboard_type is required to reverse url back to dashboard
        if not hasattr(self, 'dashboard_type'):
            raise AttributeError('{0} attribute \'dashboard_type\' is required but has not been defined.'.format(self))
        elif not self.dashboard_type:
            raise ValueError('{0} attribute \'dashboard_type\' cannot be None. '.format(self))
        else:
            pass

        # requisition_model is required to update ScheduledLabEntryBucket,
        # but if not defined will pass
        if hasattr(self, 'requisition_model'):
            from lab_requisition.models import BaseBaseRequisition
            #if not set([BaseRequisition, BaseBaseRequisition]).intersection(set(self.requisition_model.__bases__)):
            if not issubclass(self.requisition_model, BaseBaseRequisition):
                raise ValueError('{0} attribute \'requisition_model\' must be an instance of lab_requisition.models.BaseRequisition.'.format(self))

        super(BaseAppointmentModelAdmin, self).__init__(*args, **kwargs)

        # appointment key should exist, if not, maybe sent the wrong model
        if not [f.name for f in self.model._meta.fields if f.name == 'appointment']:
            raise AttributeError('The model for BaseAppointmentModelAdmin child class {0} '
                                 'requires model attribute \'appointment\'. Not found '
                                 'in model {1}.'.format(self, self.model._meta.object_name))

        self.list_display = ['appointment', 'report_datetime', 'reason', 'created',
                             'modified', 'user_created', 'user_modified', ]

        self.search_fields = ['id', 'reason', 'appointment__visit_definition__code',
                              'appointment__registered_subject__subject_identifier']

        self.list_filter = ['appointment__visit_instance',
                            'reason',
                            'appointment__visit_definition__code',
                            'appointment__registered_subject__study_site__site_code',
                            'report_datetime',
                            'created',
                            'modified',
                            'user_created',
                            'user_modified',
                            'hostname_created']

    def save_model(self, request, obj, form, change):
        #scheduled_entry = ScheduledEntry()
        #scheduled_entry.add_or_update_for_visit(visit_model_instance=obj)
        # if requisition_model has been defined, assume scheduled labs otherwise pass
        if hasattr(self, 'requisition_model'):
            ScheduledLabEntryBucket = get_model('bhp_lab_entry', 'scheduledlabentrybucket')
            ScheduledLabEntryBucket.objects.add_for_visit(
                visit_model_instance=obj,
                requisition_model=self.requisition_model,
                )
        return super(BaseAppointmentModelAdmin, self).save_model(request, obj, form, change)

#     def delete_model(self, request, obj):
#         return super(BaseAppointmentModelAdmin, self).delete_model(request, obj)

#     def delete_view(self, request, object_id, extra_context=None):
# 
#         appointment = self.model.objects.get(pk=object_id).appointment.pk
#         subject_identifier = self.model.objects.get(pk=object_id).appointment.registered_subject.subject_identifier
#         result = super(BaseAppointmentModelAdmin, self).delete_view(request, object_id, extra_context)
#         context = {'dashboard_type': self.dashboard_type, 'appointment': appointment}
#         if subject_identifier:
#             context['subject_identifier'] = subject_identifier
#         if extra_context:
#             for k, v in extra_context.items():
#                 context[k] = v
#         result['Location'] = reverse('dashboard_url', kwargs=context)
#         return result

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        from bhp_appointment.models import Appointment
        if db_field.name == 'appointment' and request.GET.get('appointment'):
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment', 0))
        return super(BaseAppointmentModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
