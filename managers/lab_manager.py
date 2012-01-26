from datetime import datetime
from django.db import models
from django.db.models import Q, Max
from django.core.urlresolvers import reverse
from django.conf import settings
from bhp_common.models import MyBasicUuidModel
from lab_aliquot_list.models import AliquotCondition
from lab_result.models import Result as LisResult
from lab_receive.models import Receive as LisReceive
from lab_result_item.models import ResultItem as LisResultItem
from bhp_poll_mysql.poll_mysql import PollMySQL
from lab_clinic_api.models import UpdateLog


class LabManager(models.Manager):

    def connected(self):
        host = settings.DATABASES['lab_api']['HOST']
        if not host:
            host = 'localhost'
            
        port = settings.DATABASES['lab_api']['PORT']
        if not port:
            port = '3306'
            
        poll = PollMySQL(host, int(port))
        
        return poll.is_server_active()
    
    def update(self, **kwargs ):

        """
        Using the 'lab_api' DATABASE connection defined in settings, update the local copy of lab data and return nothing.
        
        From your code, call 'fetch' instead of 'update'
        """
         
        # check dmis for any new results
         
         
        subject_identifier = kwargs.get('subject_identifier')
        if self.connected():
            # update for new samples received at the lab
            lis_receives = LisReceive.objects.using('lab_api').filter(patient__subject_identifier=subject_identifier).exclude(aliquot__order__result__isnull=True)
            for lis_receive in lis_receives:
                if AliquotCondition.objects.filter(display_index=lis_receive.receive_condition):
                    aliquot_condition = AliquotCondition.objects.get(display_index=lis_receive.receive_condition) 
                    condition_name = aliquot_condition.name[0:35]                       
                else:
                    condition_name = lis_receive.receive_condition 
                if super(LabManager, self).filter(subject_identifier=subject_identifier, receive_identifier=lis_receive.receive_identifier, aliquot_identifier__isnull=True):
                    lab = super(LabManager, self).get(subject_identifier=subject_identifier, receive_identifier=lis_receive.receive_identifier, aliquot_identifier__isnull=True)
                    lab.modified = datetime.today()
                    lab.user_created = 'auto'
                    lab.user_modified = 'auto'
                    lab.hostname_created = 'auto'
                    lab.hostname_modified = 'auto'
                    lab.subject_identifier = subject_identifier
                    lab.clinician_initials = lis_receive.clinician_initials
                    lab.protocol_identifier = lis_receive.protocol.protocol_identifier
                    lab.release_status = 'received' 
                    lab.panel = lis_receive.dmis_panel_name
                    lab.aliquot_identifier = None #lis_receive.aliquot.aliquot_identifier
                    lab.condition = condition_name
                    lab.receive_datetime = lis_receive.receive_datetime
                    lab.receive_identifier = lis_receive.receive_identifier
                    lab.order_identifier = None 
                    lab.order_datetime = None
                    lab.result_identifier = None
                    lab.drawn_datetime = lis_receive.drawn_datetime
                    lab.release_datetime = None

                    lab.save()
                    #print 'receive: updating %s for %s' % (lis_receive.receive_identifier, subject_identifier)
                else:
                    super(LabManager, self).create(
                        created = lis_receive.created,
                        modified = lis_receive.modified,
                        user_created = lis_receive.user_created,
                        user_modified = lis_receive.user_modified,
                        hostname_created = lis_receive.hostname_created,
                        hostname_modified = lis_receive.hostname_modified,
                        subject_identifier = subject_identifier,
                        protocol_identifier = lis_receive.protocol.protocol_identifier,
                        clinician_initials = lis_receive.clinician_initials,
                        release_status = 'received',
                        panel = lis_receive.dmis_panel_name,
                        drawn_datetime = lis_receive.drawn_datetime,
                        receive_datetime = lis_receive.receive_datetime,
                        receive_identifier = lis_receive.receive_identifier,
                        aliquot_identifier = None, #lis_receive.aliquot.aliquot_identifier,
                        condition = condition_name,

                        )
                    #print 'receive: creating %s for %s' % (lis_receive.receive_identifier, subject_identifier)                        
                
                                                    
            # order and result
            qset = Q(order__aliquot__receive__patient__subject_identifier=subject_identifier)
            aggr = super(LabManager, self).filter(subject_identifier=subject_identifier).aggregate(Max('release_datetime'))
            last_release_datetime = aggr['release_datetime__max']
            #if last_release_datetime:
            #    qset.add(Q(release_datetime__gt=last_release_datetime), Q.AND)

            lis_results = LisResult.objects.using('lab_api').filter(qset)

            # check release_datetime and create new or update modified records            
            for lis_result in lis_results:         
                if super(LabManager, self).filter(subject_identifier=subject_identifier, receive_identifier=lis_result.order.order_identifier):
                    lab = super(LabManager, self).get(subject_identifier=subject_identifier, order_identifier=lis_result.order.order_identifier)
                    lab.modified = datetime.today()
                    lab.user_created = 'auto'
                    lab.user_modified = 'auto'
                    lab.hostname_created = 'auto'
                    lab.hostname_modified = 'auto'
                    lab.subject_identifier = subject_identifier
                    lab.clinician_initials = lis_result.order.aliquot.receive.clinician_initials
                    lab.protocol_identifier = lis_result.order.aliquot.receive.protocol.protocol_identifier
                    lab.release_status = lis_result.release_status
                    lab.panel = lis_result.order.panel.name
                    lab.aliquot_identifier = lis_result.order.aliquot.aliquot_identifier
                    lab.condition = lis_result.order.aliquot.condition.name
                    lab.receive_datetime = lis_result.order.aliquot.receive.receive_datetime
                    lab.receive_identifier = lis_result.order.aliquot.receive.receive_identifier
                    lab.order_identifier = lis_result.order.order_identifier                
                    lab.order_datetime = lis_result.order.order_datetime                                            
                    lab.result_identifier = lis_result.result_identifier                                    
                    lab.drawn_datetime = lis_result.order.aliquot.receive.drawn_datetime
                    lab.release_datetime = lis_result.release_datetime
                    lab.save()
                    #print 'order: updating %s for %s' % (lis_result.order.aliquot.receive.receive_identifier, subject_identifier)                    
            
                else:
                    lab = super(LabManager, self).create(
                        created = datetime.today(),
                        modified = datetime.today(),
                        user_created = 'auto',
                        user_modified = 'auto',
                        hostname_created = 'auto',
                        hostname_modified = 'auto',
                        subject_identifier = subject_identifier,
                        clinician_initials = lis_result.order.aliquot.receive.clinician_initials,                        
                        protocol_identifier = lis_result.order.aliquot.receive.protocol.protocol_identifier,                        
                        release_status = lis_result.release_status,
                        panel = lis_result.order.panel.name,
                        aliquot_identifier = lis_result.order.aliquot.aliquot_identifier,
                        condition = lis_result.order.aliquot.condition.name,
                        receive_datetime = lis_result.order.aliquot.receive.receive_datetime,
                        receive_identifier = lis_result.order.aliquot.receive.receive_identifier,
                        order_identifier = lis_result.order.order_identifier,  
                        order_datetime = lis_result.order.order_datetime,                        
                        result_identifier = lis_result.result_identifier,
                        drawn_datetime = lis_result.order.aliquot.receive.drawn_datetime,
                        release_datetime = lis_result.release_datetime,
                        )
                    #print 'order: creating %s for %s' % (lis_result.order.aliquot.receive.receive_identifier, subject_identifier)                                                
            if UpdateLog.objects.filter(subject_identifier=subject_identifier):
                update_log = UpdateLog.objects.get(subject_identifier=subject_identifier)
                update_log.update_datetime = datetime.today()                 
                update_log.save()
            else:
                UpdateLog.objects.create(subject_identifier=subject_identifier, update_datetime=datetime.today())                
                
                
            # requisition
            # check that the requisition information in scheduled_lab_entry is up-to-date
            # update status of requisition based on specimen identifier and panel and drawn-datetime    
            # create the requisition if it does not exist (e.g specimen identifier was determined at the lab)
            
                           
        # return super(LabManager, self).filter(subject_identifier = subject_identifier)                

    def fetch(self, **kwargs):
        """
        Update and Fetch the local copy of lab data for a given subject_identifier.
        """
        subject_identifier = kwargs.get('subject_identifier')

        qset = Q(subject_identifier = subject_identifier)

        # update the local copy of results for this subject
        self.update(subject_identifier = subject_identifier)
        
        # return filtered model instance
        return super(LabManager, self).filter((qset))

