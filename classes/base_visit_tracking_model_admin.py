from django.db.models import ForeignKey
from django.core.urlresolvers import reverse
from bhp_base_model.classes import BaseModelAdmin
from bhp_entry.models import ScheduledEntryBucket
from bhp_export_data.actions import export_as_csv_action
from visit_model_helper import VisitModelHelper
from bhp_visit_tracking.actions import update_entry_bucket_rules


class BaseVisitTrackingModelAdmin(BaseModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to your visit model(s)

    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()

    """

    visit_model = None

    def __init__(self, *args, **kwargs):

        super(BaseVisitTrackingModelAdmin, self).__init__(*args, **kwargs)

        model = args[0]

        if not self.visit_model:
            raise ValueError, "BaseVisitModelAdmin for %s needs a visit model. None found. Please correct." % (model,)
        self.visit_model_foreign_key = [fk for fk in [f for f in model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if not self.visit_model_foreign_key:
            raise ValueError, "The model for %s requires a foreign key to visit model %s. None found. Either correct the model or change the ModelAdmin class." % (self, self.visit_model)
        else:
            self.visit_model_foreign_key = self.visit_model_foreign_key[0].name

        self.search_fields = ['id', self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier', ]

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
            'hostname_created',
            ]

        self.actions.append(export_as_csv_action("CSV Export: ...with visit and demographics",
            fields=[],
            exclude=['id', ],
            extra_fields=[
                {'report_datetime': '%s__report_datetime' % self.visit_model_foreign_key },
                {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier'},
                {'gender': self.visit_model_foreign_key + '__appointment__registered_subject__gender'},
                {'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob'},
                {'visit_reason': self.visit_model_foreign_key + '__reason'},
                {'visit_status': self.visit_model_foreign_key + '__appointment__appt_status'},
                {'visit': self.visit_model_foreign_key + '__appointment__visit_definition__code'},
                {'visit_instance': self.visit_model_foreign_key + '__appointment__visit_instance'},
                ],
            ))

        self.actions.append(update_entry_bucket_rules)



    def save_model(self, request, obj, form, change):

        if not self.visit_model:
            raise AttributeError, 'visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''

        # whatever this does, the post_save signal may call
        # bucket.py class to override
        ScheduledEntryBucket.objects.update_status(
            model_instance=obj,
            visit_model=self.visit_model,
            action='new',
            )

        return super(BaseVisitTrackingModelAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):

        if not self.visit_model:
            raise AttributeError, 'delete_model(): visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''

        ScheduledEntryBucket.objects.update_status(
            model_instance=obj,
            visit_model=self.visit_model,
            action='delete',
            )

        return super(BaseVisitTrackingModelAdmin, self).delete_model(request, obj)

    def delete_view(self, request, object_id, extra_context=None):

        """ Tries to redirect if enough information is available in the admin model."""

        if not self.visit_model:
            raise AttributeError('visit_model cannot be None. Specify in the ModelAdmin class. '
                                 'e.g. visit_model = \'maternal_visit\'')
        if not self.dashboard_type:
            raise AttributeError('dashboard_type cannot be None. Specify in the ModelAdmin '
                                 'class. e.g. dashboard_type = \'subject\'')
            self.dashboard_type = 'subject'
        visit_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name][0].name
        pk = self.model.objects.values(visit_fk_name).get(pk=object_id)
        visit_instance = self.visit_model.objects.get(pk=pk[visit_fk_name])
        subject_identifier = visit_instance.appointment.registered_subject.subject_identifier
        visit_code = visit_instance.appointment.visit_definition.code
        result = super(BaseVisitTrackingModelAdmin, self).delete_view(request, object_id, extra_context)
        result['Location'] = reverse('dashboard_visit_url', kwargs={'dashboard_type': self.dashboard_type,
                                                                     'subject_identifier': subject_identifier,
                                                                     'appointment': visit_instance.appointment.pk,
                                                                     'visit_code': unicode(visit_code)})
        return result

#    def delete_view(self, request, object_id, extra_context=None):
#
#        kwargs = {}
#        next_url = None
#        if self.dashboard_type:
#            kwargs = {'dashboard_type': self.dashboard_type}
#            next_url_name = 'dashboard_url'
#            try:
#                #try for subject_identifier, registered_subject or a visit_model
#                if 'registered_subject' in [field.attname for field in self.model._meta.fields]:
#                    kwargs['registered_subject'] = self.model.objects.get(pk=object_id).registered_subject.pk
#                elif 'visit_model' in dir(self) and 'visit_fieldname' in dir(self):
#                    next_url_name = 'dashboard_visit_url'
#                    field_name = self.visit_fieldname
#                    visit_model_instance = getattr(self.model.objects.get(pk=object_id), field_name)
#                    kwargs['subject_identifier'] = visit_model_instance.appointment.registered_subject.subject_identifier
#                    kwargs[self.visit_fieldname] = visit_model_instance.pk
#                    kwargs['visit_vode'] = visit_model_instance.visit_definition.code
#                    kwargs['visit_instance'] = visit_model_instance.visit_instance
#                #elif 'subject_identifier' in [field.attname for field in self.model._meta.fields]:
#                #    kwargs['registered_subject'] = visit_model_instance.appointment.registered_subject.pk
#                else:
#                    pass
#                next_url = reverse(next_url_name, kwargs=kwargs)
#            except NoReverseMatch:
#                print 'warning: delete_view failed to reverse \'{0}\' with kwargs {1}'.format(next_url_name, kwargs)
#                next_url = None
#                pass
#            except:
#                raise
#        result = super(BaseModelAdmin, self).delete_view(request, object_id, extra_context)
#        if next_url:
#            result['Location'] = next_url
#
#        return result



    #override, limit dropdown in add_view to id passed in the URL
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        visit_model_helper = VisitModelHelper()
        if db_field.name == visit_model_helper.get_visit_field(model=self.model, visit_model=self.visit_model):
            kwargs["queryset"] = visit_model_helper.set_visit_queryset(
                                                            subject_identifier=request.GET.get('subject_identifier', 0),
                                                            visit_code=request.GET.get('visit_code', 0),
                                                            visit_instance=request.GET.get('visit_instance', 0),
                                                            )

        return super(BaseVisitTrackingModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

