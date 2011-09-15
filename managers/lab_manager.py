from datetime import datetime
from django.db import models
from django.db.models import Q, Max
from django.core.urlresolvers import reverse
from django.conf import settings
from bhp_common.models import MyBasicUuidModel
from lab_result.models import Result as LisResult
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
         
        subject_identifier = kwargs.get('subject_identifier')

        if self.connected():
            qset = Q(order__aliquot__receive__patient__subject_identifier = subject_identifier)
            
            aggr = super(LabManager, self).filter(subject_identifier = subject_identifier).aggregate(Max('release_datetime'))
            last_release_datetime = aggr['release_datetime__max']
            
            if last_release_datetime:
                qset.add(Q(release_datetime__gt = last_release_datetime), Q.AND)

            lis_results = LisResult.objects.using('lab_api').filter(qset)

            # check release_datetime and create new or update modified records            
            for lis_result in lis_results:         
                if super(LabManager, self).filter(subject_identifier = subject_identifier, order_identifier = lis_result.order.order_identifier):
                    lab = super(LabManager, self).get(subject_identifier = subject_identifier, order_identifier = lis_result.order.order_identifier)
                    lab.modified = datetime.today()
                    lab.user_created = 'auto'
                    lab.user_modified = 'auto'
                    lab.hostname_created = 'auto'
                    lab.hostname_modified = 'auto'
                    lab.subject_identifier = subject_identifier
                    lab.clinician_initials = lis_result.order.aliquot.receive.clinician_initials
                    lab.protocol_identifier = lis_result.order.aliquot.receive.protocol
                    lab.release_status = lis_result.release_status
                    lab.panel = lis_result.order.panel
                    lab.aliquot_identifier = lis_result.order.aliquot.aliquot_identifier
                    lab.condition = lis_result.order.aliquot.condition
                    lab.receive_datetime = lis_result.order.aliquot.receive.receive_datetime
                    lab.receive_identifier = lis_result.order.aliquot.receive.receive_identifier
                    lab.order_identifier = lis_result.order.order_identifier                
                    lab.result_identifier = lis_result.result_identifier                                    
                    lab.drawn_datetime = lis_result.order.aliquot.receive.datetime_drawn
                    lab.release_datetime = lis_result.release_datetime
                    lab.save()
            
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
                        protocol_identifier = lis_result.order.aliquot.receive.protocol,                        
                        release_status = lis_result.release_status,
                        panel = lis_result.order.panel,
                        aliquot_identifier = lis_result.order.aliquot.aliquot_identifier,
                        condition = lis_result.order.aliquot.condition,
                        receive_datetime = lis_result.order.aliquot.receive.receive_datetime,
                        receive_identifier = lis_result.order.aliquot.receive.receive_identifier,
                        order_identifier = lis_result.order.order_identifier,  
                        result_identifier = lis_result.result_identifier,
                        drawn_datetime = lis_result.order.aliquot.receive.datetime_drawn,
                        release_datetime = lis_result.release_datetime,
                        )
            if UpdateLog.objects.filter(subject_identifier=subject_identifier):
                update_log = UpdateLog.objects.get(subject_identifier=subject_identifier)
                update_log.update_datetime = datetime.today()                 
                update_log.save()
            else:
                UpdateLog.objects.create(subject_identifier=subject_identifier, update_datetime=datetime.today())                
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

