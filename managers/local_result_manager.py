from datetime import datetime
from django.db import models
from django.db.models import Q, Max
from django.core.urlresolvers import reverse
from django.conf import settings
from bhp_common.models import MyBasicUuidModel
from lab_result.models import Result
from bhp_poll_mysql.poll_mysql import PollMySQL


class LocalResultManager(models.Manager):

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
            
            aggr = super(LocalResultManager, self).filter(subject_identifier = subject_identifier).aggregate(Max('release_datetime'))
            last_release_datetime = aggr['release_datetime__max']
            
            if last_release_datetime:
                qset.add(Q(release_datetime__gt = last_release_datetime), Q.AND)

            results = Result.objects.using('lab_api').filter(qset)
        
            # check release_datetime and create new or update modified records            
            for r in results:
                if super(LocalResultManager, self).filter(subject_identifier = subject_identifier, order_identifier = r.order.order_identifier):
                    obj = super(LocalResultManager, self).get(subject_identifier = subject_identifier, order_identifier = r.order.order_identifier)
                    
                    obj.modified = datetime.today()
                    obj.user_created = 'auto'
                    obj.user_modified = 'auto'
                    obj.hostname_created = 'auto'
                    obj.hostname_modified = 'auto'
                    obj.subject_identifier = subject_identifier
                    obj.release_status = r.release_status
                    obj.panel = r.order.panel
                    obj.aliquot_identifier = r.order.aliquot.aliquot_identifier
                    obj.receive_datetime = r.order.aliquot.receive.receive_datetime
                    obj.receive_identifier = r.order.aliquot.receive.receive_identifier
                    obj.order_identifier = r.order.order_identifier                
                    obj.drawn_datetime = r.order.aliquot.receive.datetime_drawn
                    obj.release_datetime = r.release_datetime
                    obj.save()
            
                else:
                    super(LocalResultManager, self).create(
                        created = datetime.today(),
                        modified = datetime.today(),
                        user_created = 'auto',
                        user_modified = 'auto',
                        hostname_created = 'auto',
                        hostname_modified = 'auto',
                        subject_identifier = subject_identifier,
                        release_status = r.release_status,
                        panel = r.order.panel,
                        aliquot_identifier = r.order.aliquot.aliquot_identifier,
                        receive_datetime = r.order.aliquot.receive.receive_datetime,
                        receive_identifier = r.order.aliquot.receive.receive_identifier,
                        order_identifier = r.order.order_identifier,  
                        drawn_datetime = r.order.aliquot.receive.datetime_drawn,
                        release_datetime = r.release_datetime,
                        )

        # return super(LocalResultManager, self).filter(subject_identifier = subject_identifier)                

    def fetch(self, **kwargs):
        """
        Update and Fetch the local copy of lab data for a given subject_identifier.
        """
        subject_identifier = kwargs.get('subject_identifier')

        qset = Q(subject_identifier = subject_identifier)

        # update the local copy of results for this subject
        self.update(subject_identifier = subject_identifier)
        
        # return filtered model instance
        return super(LocalResultManager, self).filter((qset))

