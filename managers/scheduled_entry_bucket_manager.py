from datetime import datetime
from django.db import models
from django.db.models import ForeignKey
from bhp_common.models import ContentTypeMap
from bhp_entry.models import Entry

class ScheduledEntryBucketManager(models.Manager):

    def get_scheduled_forms_for(self, **kwargs ):
    
        """Return a queryset of ScheduledEntryBucket objects for the given subject and appointment.
        
        Note that ScheduledEntryBucket objects are linked to a subject's appointment 
        for visit_instance = '0'; that is, the first appointment for 
        a timepoint/visit. """

        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError("Manager get_schedule_forms_for expected registered_subject. Got None.") 

        appt_0 = kwargs.get("appointment")
        #if not visit_code:
        #    raise TypeError("Manager get_schedule_forms_for expected appointment of visit instance 0. Got None.")

        visit_code = kwargs.get("visit_code")        
        if not visit_code:
            raise TypeError("Manager get_schedule_forms_for expected visit_code. Got None.")
             
        #appointment = Appointment.objects.get(
        #    registered_subject = registered_subject, 
        #    visit_definition__code = visit_code,
        #    visit_instance = '0'            
        #    )

        if appt_0:    
            # scheduled_entry_bucket lists records based on appointment at visit instance 0
            # get the the appointment for visit_instance = '0'

            #appt = Appointment.objects.filter(
            #    registered_subject = registered_subject, 
            #    visit_definition__code = appointment.visit_definition.code, 
            #    visit_instance = '0'
            #    )
            # get the scheduled crfs based on the appt for visit_instance = '0'   
            
            scheduled_entry_bucket = super(ScheduledEntryBucketManager, self).filter(
                                                registered_subject = registered_subject, 
                                                appointment = appt_0,
                                                ).order_by('entry__entry_order')
        else:
            scheduled_entry_bucket = super(ScheduledEntryBucketManager, self).none()         
            
        return scheduled_entry_bucket


    def add_for_visit(self, **kwargs):
        
        """ Add entries to the scheduled_entry_bucket for a given visit_model. 
        
        
        for example, 
        
        class VisitAdmin(MyRegisteredSubjectModelAdmin):

            form = VisitForm

            def save_model(self, request, obj, form, change):

                ScheduledEntryBucket.objects.add_for_visit(
                    visit_model_instance = obj,
                    visit_model_instance_field = 'visit',                
                    qset = Q(visit=obj),
                    )                
                    
                return super(VisitAdmin, self).save_model(request, obj, form, change)                                                
                
            search_fields = ('appointment__registered_subject__subject_identifier',)        
        
        """

        visit_model_instance = kwargs.get('visit_model_instance')
        visit_model_instance_field = kwargs.get('visit_model_instance_field')
        qset = kwargs.get('qset')                
        
        # scheduled forms have a foreign key to a visit_model_instance
        # qset, in this case, is a filter on the visit_model_instance for each entry model
        #   for example for entry model maternal_arv_preg qset = Q(maternal_visit=obj) where obj was current model instance (obj) in save_model in admin.py

        # confirm visit_model_instance has a "appointment" field/model attribute
        if 'appointment' not in [f.name for f in visit_model_instance._meta.fields if f.name=='appointment']:
            raise AttributeError, "ScheduledEntryBucketManager expects model %s to have attribute \'appointment\'." % visit_model_instance._meta.object_name  
        
        registered_subject = visit_model_instance.appointment.registered_subject

        if kwargs.get('subject_visit_model'):
            raise ValueError('subject_visit_model has been changed to \'visit_model_instance\', please read comment in ScheduledEntryBucketManager.add_for_visit() and correct.')


        # scheduled entries are only added if visit instance is 0
        if visit_model_instance.appointment.visit_instance == '0':
        
            filled_datetime = datetime.today()
            report_datetime = visit_model_instance.report_datetime
                            
            # fetch entries required for this the visit definition of this visit_model_instance.appointment
            entries = Entry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition)

            for entry in entries:

                # calculate due date -- "needs work"
                due_datetime = entry.visit_definition.get_upper_window_datetime(report_datetime)                                

                # check if entry.entry_form.model has been keyed for this registered_subject, timepoint
                # if so, set report date and status accordingly
                # model must have field of value visit_model_instance_field, otherwise ignore
                if visit_model_instance_field in [f.name for f in entry.content_type_map.model_class()._meta.fields]:
                
                    if not super(ScheduledEntryBucketManager, self).filter(
                                    registered_subject = registered_subject, 
                                    appointment = visit_model_instance.appointment, 
                                    entry = entry):                        
                        # not in bucket, but should be, so add to bucket
                        super(ScheduledEntryBucketManager, self).create(
                                registered_subject=registered_subject,
                                appointment = visit_model_instance.appointment,
                                entry = entry,
                                current_entry_title = entry.content_type_map.model_class()._meta.verbose_name,
                                fill_datetime = filled_datetime,
                                due_datetime = due_datetime,                      
                                )
                
                    if entry.content_type_map.model_class().objects.filter(qset):
                        #entry_model = entry.content_type_map.model_class().objects.get(qset)
                        report_datetime = visit_model_instance.report_datetime

                        # add to bucket, if not already added, or update
                        if super(ScheduledEntryBucketManager, self).filter(
                                    registered_subject = registered_subject, 
                                    appointment = visit_model_instance.appointment, 
                                    entry = entry):
                            # already in bucket, so get bucket entry
                            s = super(ScheduledEntryBucketManager, self).get(
                                        registered_subject = registered_subject, 
                                        appointment = visit_model_instance.appointment, 
                                        entry = entry)
                            # update report_date
                            s.report_datetime = report_datetime
                            # update status if NEW only, (may be queried or something)
                            if s.entry_status == 'NEW':
                                s.entry_status = 'KEYED'
                            # save
                            s.save()

    def update_status(self, **kwargs):

        """Update bucket status, etc for a given entry in bucket. 
        
        
        for example
        
        
        def save_model(self, request, obj, form, change):
            
            ScheduledEntryBucket.objects.update_status(
                model = obj,
                visit_model_instance = obj.visit,
                )
                            
            return super(MyVisitModelAdmin, self).save_model(request, obj, form, change)
            
        def delete_model(self, request, obj):

            ScheduledEntryBucket.objects.update_status(
                model = obj,
                action = 'delete',
                visit_model_instance = obj.visit,
                )
                
            return super(MyVisitModelAdmin, self).delete_model(request, obj)         
        
        """    

        
        model_instance = kwargs.get('model')    
        visit_model = kwargs.get('visit_model')                
        if not visit_model:
            raise AttributeError, 'ScheduledEntryBucketManager.update_status requires attribute \'visit_model\'. Got None'
            
        # in this model_instance find the foreignkey field to the visit_model
        visit_fk = [fk for fk in [f for f in model_instance._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == visit_model._meta.module_name]
        # get the name + _id.
        visit_fk_name = '%s_id' % visit_fk[0].name 
        # query for the visit model instance
        visit_model_instance = visit_model.objects.get(pk = model_instance.__dict__[visit_fk_name])
        
        default_validation_error_msg = "Entry exists for '%s'. Please correct before updating this form." % model_instance._meta.verbose_name        
        visit_model_instance = kwargs.get('visit_model_instance')
        if kwargs.get('subject_visit_model'):
            raise AttributeError('subject_visit_model should be \'visit_model_instance\', please correct call to update_status')
        action = kwargs.get('action', 'add_change')
        comment = kwargs.get('comment', '----')
        model_filter_qset = kwargs.get('model_filter_qset')
        model_filter_validation_error_msg = kwargs.get('model_filter_validation_error_msg', default_validation_error_msg)
        
        
        # get contenttype for given model_instance
        content_type_map = ContentTypeMap.objects.get(app_label = model_instance._meta.app_label, name = model_instance._meta.verbose_name)
        
        if visit_model_instance:
            # get visit definition for visit_model_instance attached to this model
            visit_definition = visit_model_instance.appointment.visit_definition
            # get Entry using visit_definition and content_type_map 
            entry = Entry.objects.filter(visit_definition = visit_definition, content_type_map = content_type_map)        
            # check if entry.content_type_map.model has been keyed for this registered_subject, timepoint
            # if so, set report date and status accordingly
            report_datetime = visit_model_instance.report_datetime
            registered_subject = visit_model_instance.appointment.registered_subject
            appointment = visit_model_instance.appointment.__class__.objects.get(
                registered_subject = registered_subject, 
                visit_definition__code = visit_model_instance.appointment.visit_definition.code, 
                visit_instance = '0')
            # update

            if super(ScheduledEntryBucketManager, self).filter(registered_subject = registered_subject, appointment = appointment, entry = entry):
                # already in bucket, so get bucket entry
                s = super(ScheduledEntryBucketManager, self).get(registered_subject = registered_subject, appointment = appointment, entry = entry)
                # update status if NEW no matter what, to indictate perhaps that it was modified

                if action == 'add_change':
                    s.report_datetime = report_datetime
                    s.entry_status = 'KEYED'
                    s.entry_comment = ''                
                elif action == 'delete':
                    s.report_datetime = None
                    s.entry_status = 'NEW'
                    s.entry_comment = 'deleted'
                elif action == 'new':
                    s.report_datetime = None
                    s.entry_status = 'NEW'
                    s.entry_comment = 'required'
                elif action == 'not_required':
                    s.report_datetime = None
                    s.entry_status = 'NOT_REQUIRED'
                    s.entry_comment = ''
                    #if content_type_map.model_class().objects.filter(model_filter_qset):
                        #raise forms.ValidationError(model_filter_validation_error_msg)
                else:
                        if s.entry_status == 'MISSED' or s.entry_status == 'NEW' or s.entry_status == 'PENDING' or s.entry_status == 'NOT_REQUIRED':
                            s.report_datetime = None
                            s.entry_status = 'NOT_REQUIRED'
                            s.entry_comment = comment
                        else:
                            raise TypeError("ScheduledEntryBucketManager cannot change value of attribute entry_status to 'not required' when entry_status = '%s'. Test the value in the form for model '%s' first." % (model_instance._meta.verbose_name,s.entry_status))    
                # clear close_datetime
                s.close_datetime = None
                s.modified = datetime.today()
                # save
                s.save()

