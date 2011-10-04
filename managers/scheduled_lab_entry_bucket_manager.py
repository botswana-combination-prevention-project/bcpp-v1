from datetime import datetime
from django.db import models
from django.db.models import ForeignKey, get_model, Q
from django.db.models.base import ModelBase
from bhp_content_type_map.models import ContentTypeMap
from bhp_entry.managers import BaseEntryBucketManager
from bhp_lab_entry.models import LabEntry


class ScheduledLabEntryBucketManager(BaseEntryBucketManager):

    def get_scheduled_labs_for(self, **kwargs ):
    
        """Return a queryset of ScheduledLabEntryBucket objects for the given subject and appointment.
        
        Note that ScheduledLabEntryBucket objects are linked to a subject's appointment 
        for visit_instance = '0'; that is, the first appointment for 
        a timepoint/visit. """
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError("Manager get_schedule_lab_entries_for expected registered_subject. Got None.") 
        appt_0 = kwargs.get("appointment")
        visit_code = kwargs.get("visit_code")        
        if not visit_code:
            raise TypeError("Manager get_schedule_lab_entries_for expected visit_code. Got None.")
             
        if appt_0:    
            # get the scheduled crfs based on the appt for visit_instance = '0'   
            scheduled_lab_entry_bucket = super(ScheduledLabEntryBucketManager, self).filter(
                                                registered_subject = registered_subject, 
                                                appointment = appt_0,
                                                ).order_by('lab_entry__entry_order')
        else:
            scheduled_lab_entry_bucket = super(ScheduledLabEntryBucketManager, self).none()         

        return scheduled_lab_entry_bucket


    def add_for_visit(self, **kwargs):
        
        """ Add entries to the scheduled_entry_bucket for a given visit_model. 
        
        Normally called from Base model admin class BaseAppointmentModelAdmin
        
        otherwise, for example, 
        
        class VisitAdmin(MyRegisteredSubjectModelAdmin):

            form = VisitForm

            def save_model(self, request, obj, form, change):

                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance = obj,
                    requisition_model = requisition_model,                    
                    qset = Q(visit=obj),
                    )                
                    
                return super(VisitAdmin, self).save_model(request, obj, form, change)                                                
                
            search_fields = ('appointment__registered_subject__subject_identifier',)        
        
        """
        
        requisition_model = kwargs.get('requisition_model')
        if not requisition_model:
            raise AttributeError('Attribute requisition_model cannot be None for ScheduledLabEntryBucketManager.add_for_visit().')
        
        visit_model_instance = kwargs.get('visit_model_instance')
        qset = kwargs.get('qset')                
        
        # scheduled forms have a foreign key to a visit_model_instance
        # qset, in this case, is a filter on the visit_model_instance for each lab_entry

        # confirm visit_model_instance has a "appointment" field/model attribute
        if 'appointment' not in [f.name for f in visit_model_instance._meta.fields if f.name=='appointment']:
            raise AttributeError, "ScheduledLabEntryBucketManager expects model %s to have attribute \'appointment\'." % visit_model_instance._meta.object_name  

        registered_subject = visit_model_instance.appointment.registered_subject

        if kwargs.get('subject_visit_model'):
            raise ValueError('subject_visit_model has been changed to \'visit_model_instance\', please read comment in ScheduledLabEntryBucketManager.add_for_visit() and correct.')
        if kwargs.get('visit_model_instance_field'):
            raise AttributeError('Attribute visit_model_instance_field is not required when calling ScheduledLabEntryBucketManager.add_for_visit(). Please remove.')


        # scheduled lab_entrys are only added if visit instance is 0
        if visit_model_instance.appointment.visit_instance == '0':
        
            filled_datetime = datetime.today()
            report_datetime = visit_model_instance.report_datetime
                            
            # fetch entries required for this the visit definition of this visit_model_instance.appointment
            lab_entries = LabEntry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition)

            for lab_entry in lab_entries:

                # calculate due date -- "needs work"
                due_datetime = lab_entry.visit_definition.get_upper_window_datetime(report_datetime)                                

                # check if lab_entry requisition has been keyed for this registered_subject, timepoint
                # if so, set report date and status accordingly
                if not super(ScheduledLabEntryBucketManager, self).filter(
                                registered_subject = registered_subject, 
                                appointment = visit_model_instance.appointment, 
                                lab_entry = lab_entry):                        
                    # not in bucket, but should be, so add to bucket
                    super(ScheduledLabEntryBucketManager, self).create(
                            registered_subject=registered_subject,
                            appointment = visit_model_instance.appointment,
                            lab_entry = lab_entry,
                            fill_datetime = filled_datetime,
                            due_datetime = due_datetime,                      
                            )
                            
                # scheduled forms have a foreign key to a visit_model_instance
                # model must have field of value visit_model_instance_field, otherwise ignore
                visit_model_instance_field = [fk for fk in [f for f in requisition_model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == visit_model_instance._meta.module_name][0].name                        
                if not visit_model_instance_field:
                    raise AttributeError, 'Requisition model %s must have a foreignkey attribute to the visit model %s' % (requisition_model._meta.verbose_name, visit_model_instance._meta.verbose_name)
                else:
                    qset = Q(**{visit_model_instance_field:visit_model_instance})
                    # has it been keyed, if so update status            
                    if requisition_model.objects.filter(qset):
                        report_datetime = visit_model_instance.report_datetime
                        # add to bucket, if not already added, or update
                        if super(ScheduledLabEntryBucketManager, self).filter(
                                    registered_subject = registered_subject, 
                                    appointment = visit_model_instance.appointment, 
                                    lab_entry = lab_entry):
                            # already in bucket, so get bucket entry
                            s = super(ScheduledLabEntryBucketManager, self).get(
                                        registered_subject = registered_subject, 
                                        appointment = visit_model_instance.appointment, 
                                        lab_entry = lab_entry)
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
            
            ScheduledLabEntryBucket.objects.update_status(
                requisition_model = obj,
                visit_model_instance = obj.visit,
                )
                            
            return super(MyVisitModelAdmin, self).save_model(request, obj, form, change)
            
        def delete_model(self, request, obj):

            ScheduledLabEntryBucket.objects.update_status(
                requisition_model = obj,
                action = 'delete',
                visit_model_instance = obj.visit,
                )
                
            return super(MyVisitModelAdmin, self).delete_model(request, obj)         
        
        """    

        # need to determine the visit model instance and the content_type_map value for this Entry 
        # coming from 'admin' is model instance
        # coming from 'forms' is a model

        self.set_visit_model_instance(**kwargs)  
        
        if kwargs.get('subject_visit_model'):
            raise AttributeError('subject_visit_model should be \'visit_model_instance\', please correct call to update_status')
    
        self.requisition_model = kwargs.get('model_instance')
        action = kwargs.get('action', 'add_change')
        comment = kwargs.get('comment', '----')
        model_filter_qset = kwargs.get('model_filter_qset')
        
        # have requisition_model and visit_mode_instance, so good to go from here...
        if self.visit_model_instance:
            # get visit definition for visit_model_instance attached to this model
            visit_definition = self.visit_model_instance.appointment.visit_definition
            # get Entry using visit_definition and content_type_map 
            lab_entry = LabEntry.objects.filter(visit_definition = visit_definition, panel = self.requisition_model.panel)        
            # check if entry.content_type_map.model has been keyed for this registered_subject, timepoint
            # if so, set report date and status accordingly
            report_datetime = self.visit_model_instance.report_datetime
            registered_subject = self.visit_model_instance.appointment.registered_subject
            appointment = self.visit_model_instance.appointment.__class__.objects.get(
                registered_subject = registered_subject, 
                visit_definition__code = self.visit_model_instance.appointment.visit_definition.code, 
                visit_instance = '0')
            # update

            if super(ScheduledLabEntryBucketManager, self).filter(registered_subject = registered_subject, appointment = appointment, lab_entry = lab_entry):
                # already in bucket, so get bucket entry
                s = super(ScheduledLabEntryBucketManager, self).get(registered_subject = registered_subject, appointment = appointment, lab_entry = lab_entry)
                # update entry_status if NEW no matter what, to indictate perhaps that it was modified

                status = self.get_status(
                    action = action, 
                    report_datetime = report_datetime, 
                    entry_status = s.entry_status, 
                    entry_comment = comment
                    )
                
                s.report_datetime = status['report_datetime']
                s.entry_status = status['entry_status']
                s.entry_comment = status['entry_comment']                
                s.close_datetime = status['close_datetime']                
                s.modified = datetime.today()
                # save
                s.save()

