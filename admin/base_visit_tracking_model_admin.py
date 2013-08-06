from django.db.models import ForeignKey
# from django.core.urlresolvers import reverse
from bhp_base_admin.admin import BaseModelAdmin
from bhp_export_data.actions import export_as_csv_action
from bhp_visit_tracking.classes import VisitModelHelper


class BaseVisitTrackingModelAdmin(BaseModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to your visit model(s)"""

    visit_model = None

    def __init__(self, *args, **kwargs):
        super(BaseVisitTrackingModelAdmin, self).__init__(*args, **kwargs)
        model = args[0]
        if not self.visit_model:
            raise ValueError("BaseVisitModelAdmin for %s needs a visit model. None found. Please correct." % (model))
        self.visit_model_foreign_key = [fk for fk in [f for f in model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if not self.visit_model_foreign_key:
            raise ValueError("The model for %s requires a foreign key to visit model %s. None found. Either correct the model or change the ModelAdmin class." % (self, self.visit_model))
        else:
            self.visit_model_foreign_key = self.visit_model_foreign_key[0].name
        self.search_fields = ['id', self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier', self.visit_model_foreign_key + '__pk']
        self.list_display = [self.visit_model_foreign_key,
                             'created', 'modified', 'user_created', 'user_modified', ]
        self.list_filter = [
            self.visit_model_foreign_key + '__report_datetime',
            self.visit_model_foreign_key + '__reason',
            self.visit_model_foreign_key + '__appointment__appt_status',
            self.visit_model_foreign_key + '__appointment__visit_definition__code',
            self.visit_model_foreign_key + '__appointment__registered_subject__study_site__site_code',
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created']
        self.actions.append(export_as_csv_action("CSV Export: ...with visit and demographics",
            fields=[],
            exclude=['id', ],
            extra_fields=[
                {'report_datetime': '%s__report_datetime' % self.visit_model_foreign_key},
                {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier'},
                {'gender': self.visit_model_foreign_key + '__appointment__registered_subject__gender'},
                {'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob'},
                {'visit_reason': self.visit_model_foreign_key + '__reason'},
                {'visit_status': self.visit_model_foreign_key + '__appointment__appt_status'},
                {'visit': self.visit_model_foreign_key + '__appointment__visit_definition__code'},
                {'visit_instance': self.visit_model_foreign_key + '__appointment__visit_instance'}],
            ))

#     def save_model(self, request, obj, form, change):
#         if not self.visit_model:
#             raise AttributeError('visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = '
#                                  '\'maternal_visit\'')
#         return super(BaseVisitTrackingModelAdmin, self).save_model(request, obj, form, change)

#     def delete_view(self, request, object_id, extra_context=None):
#         """ Tries to redirect if enough information is available in the admin model."""
#         if not self.visit_model:
#             raise AttributeError('visit_model cannot be None. Specify in the ModelAdmin class. '
#                                  'e.g. visit_model = \'maternal_visit\'')
#         if not self.dashboard_type:
#             raise AttributeError('dashboard_type cannot be None. Specify in the ModelAdmin '
#                                  'class. e.g. dashboard_type = \'subject\'')
#             self.dashboard_type = 'subject'
#         visit_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name][0].name
#         pk = self.model.objects.values(visit_fk_name).get(pk=object_id)
#         visit_instance = self.visit_model.objects.get(pk=pk[visit_fk_name])
#         subject_identifier = visit_instance.appointment.registered_subject.subject_identifier
#         visit_code = visit_instance.appointment.visit_definition.code
#         result = super(BaseVisitTrackingModelAdmin, self).delete_view(request, object_id, extra_context)
#         result['Location'] = reverse('dashboard_visit_url', kwargs={'dashboard_type': self.dashboard_type,
#                                                                      'subject_identifier': subject_identifier,
#                                                                      'appointment': visit_instance.appointment.pk,
#                                                                      'visit_code': unicode(visit_code)})
#         return result

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        visit_model_helper = VisitModelHelper()
        if db_field.name == visit_model_helper.get_visit_field(model=self.model, visit_model=self.visit_model):
            #if not request.GET.get('subject_identifier', None):
            #    raise TypeError('Subject identifier cannot be none when accessing {0}.'.format(db_field.name))
            kwargs["queryset"] = visit_model_helper.set_visit_queryset(
                visit_model=self.visit_model,
                pk=request.GET.get(db_field.name, None),
                subject_identifier=request.GET.get('subject_identifier', 0),
                visit_code=request.GET.get('visit_code', 0),
                visit_instance=request.GET.get('visit_instance', 0))
        return super(BaseVisitTrackingModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
