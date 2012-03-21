from django.db.models import ForeignKey
from django.core.urlresolvers import reverse
from bhp_common.models import MyModelAdmin
from bhp_entry.models import ScheduledEntryBucket
from bhp_export_data.actions import export_as_csv_action
from bhp_appointment.classes import VisitModelHelper


class BaseVisitModelAdmin(MyModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to your visit model(s)
    
    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()
    
    """ 
    
    visit_model = None

    def __init__(self, *args, **kwargs):

        model = args[0]

        if not self.visit_model:
            raise ValueError, "BaseVisitModelAdmin for %s needs a visit model. None found. Please correct." % (model,)
        self.visit_model_foreign_key = [fk for fk in [f for f in model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if not self.visit_model_foreign_key:
            raise ValueError, "The model for %s requires a foreign key to visit model %s. None found. Either correct the model or change the ModelAdmin class." % (self, self.visit_model)
        else:
            self.visit_model_foreign_key = self.visit_model_foreign_key[0].name
                
        self.search_fields = ['pk', self.visit_model_foreign_key+'__appointment__registered_subject__subject_identifier',] 
        
        self.list_display = [self.visit_model_foreign_key, 
                             'created', 'modified', 'user_created', 'user_modified',]    
        
        self.list_filter = [
            self.visit_model_foreign_key+'__report_datetime', 
            self.visit_model_foreign_key+'__reason',
            self.visit_model_foreign_key+'__appointment__appt_status',
            self.visit_model_foreign_key+'__appointment__visit_definition__code',
            self.visit_model_foreign_key+'__appointment__registered_subject__study_site__site_code', 
            'created', 
            'modified', 
            'user_created',
            'user_modified',
            'hostname_created',
            ]

        self.actions.append(export_as_csv_action("CSV Export: ...with visit and demographics", 
            fields=[], 
            exclude=['id',],        
            extra_fields=[
                {'report_datetime': '%s__report_datetime' % self.visit_model_foreign_key },        
                {'subject_identifier': self.visit_model_foreign_key+'__appointment__registered_subject__subject_identifier'},
                {'gender': self.visit_model_foreign_key+'__appointment__registered_subject__gender'},
                {'dob': self.visit_model_foreign_key+'__appointment__registered_subject__dob'},                                    
                {'visit_reason': self.visit_model_foreign_key+'__reason'},
                {'visit_status': self.visit_model_foreign_key+'__appointment__appt_status'},
                {'visit': self.visit_model_foreign_key+'__appointment__visit_definition__code'},
                {'visit_instance': self.visit_model_foreign_key+'__appointment__visit_instance'},                                                                    
                ],
            ))

        super(BaseVisitModelAdmin, self).__init__(*args, **kwargs)


    def save_model(self, request, obj, form, change):
        
        if not self.visit_model:
            raise AttributeError, 'visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''            

        # whatever this does, the post_save signal may call
        # bucket.py class to override
        ScheduledEntryBucket.objects.update_status(
            model_instance = obj,
            visit_model = self.visit_model,
            action='new',
            )

        return super(BaseVisitModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        if not self.visit_model:
            raise AttributeError, 'delete_model(): visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''            

        ScheduledEntryBucket.objects.update_status(
            model_instance = obj,
            visit_model = self.visit_model,
            action = 'delete',
            )

        return super(BaseVisitModelAdmin, self).delete_model(request, obj) 

    def delete_view(self, request, object_id, extra_context=None):

        """ delete requires knowledge of the model which is not given, so get it from the form.__dict__ and reverse resolve"""

        if not self.visit_model:
            raise AttributeError, 'visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''            

        if not self.dashboard_type:
            raise AttributeError, 'dashboard_type cannot be None. Specify in the ModelAdmin class. e.g. dashboard_type = \'subject\''
            self.dashboard_type = 'subject'

        # we don't get the url quertstring like in add or change view,
        # so, we need to get information to prepare a reverse url for the result['Location'] 
        # 'cause i don't want this going back to admin
        # the information comes from visit_model as we know this model has a key to the visit
        # we have the visit_model from the parameter set in the ModelAdmin class in admin.py
        #
        #     visit_model = MaternalVisit
        #
        # but we do not know the name of the foreignkey field
        # get visit foreignkey field name
        visit_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name][0].name        
        # query the this model for the pk to visit model, returns a dictionary { field: value }
        pk = self.model.objects.values(visit_fk_name).get(pk=object_id)
        # this is the correct instance of visit model
        visit = self.visit_model.objects.get(pk=pk[visit_fk_name])        
        # get subject_identifier and visit_code for the reverse
        subject_identifier = visit.appointment.registered_subject.subject_identifier
        visit_code = visit.appointment.visit_definition.code

        # oh yeah, call super
        result = super(BaseVisitModelAdmin, self).delete_view(request, object_id, extra_context)

        # do the reverse manually
        # if later wish to decouple from dashboard, perhaps test for dashboard_type, if none/exception skip
        result['Location'] = reverse('dashboard_visit_url' , kwargs={'dashboard_type':self.dashboard_type, 'subject_identifier':subject_identifier, 'visit_code': unicode(visit_code)})

        return result

                                                                                                        
        
    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        visit_model_helper = VisitModelHelper()
        if db_field.name == visit_model_helper.get_visit_field(model=self.model, visit_model=self.visit_model):
            kwargs["queryset"] = visit_model_helper.set_visit_queryset(
                                                            subject_identifier = request.GET.get('subject_identifier', 0),
                                                            visit_code = request.GET.get('visit_code', 0),
                                                            visit_instance = request.GET.get('visit_instance', 0),
                                                            )
        
        return super(BaseVisitModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

