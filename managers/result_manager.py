from datetime import datetime
from django.db import models
from django.conf import settings
from lab_result.models import Result as LisResult
#from bhp_poll_mysql.poll_mysql import PollMySQL
from lab_clinic_api.models import UpdateLog


class ResultManager(models.Manager):

#    def connected(self):
#        host = settings.DATABASES['lab_api']['HOST']
#        if not host:
#            host = 'localhost'
#        port = settings.DATABASES['lab_api']['PORT']
#        if not port:
#            port = '3306'
#        poll = PollMySQL(host, int(port))
#        return poll.is_server_active()

    def update(self, **kwargs):
        """
        Using the 'lab_api' DATABASE connection defined in settings, update the
        local copy of lab data and return nothing.

        From your code, call 'fetch' instead of 'update'
        """
        subject_identifier = kwargs.get('subject_identifier')
        labs = kwargs.get('labs')
        #if self.connected():
        for lab in labs:
            # update local "Result" and "ResultItem"
            lis_result = LisResult.objects.using('lab_api').filter(result_identifier=lab.result_identifier)
            if lis_result:
                if super(ResultManager, self).filter(result_identifier=lis_result[0].result_identifier):
                    result = super(ResultManager, self).get(result_identifier=lis_result[0].result_identifier)
                    for field in super(ResultManager, self).__dict__['model']._meta.fields:
                        if field.name != 'id' and field.name != 'lab':
                            result.__dict__[field.name] = lis_result[0].__dict__[field.name]
                            result.lab = lab
                        result.save()
                else:
                    kw = {}
                    for field in super(ResultManager, self).__dict__['model']._meta.fields:
                        if field.name != 'id' and field.name != 'lab':
                            kw[field.name] = lis_result[0].__dict__[field.name]
                        kw['lab'] = lab
                    result = super(ResultManager, self).create(**kw)
        if UpdateLog.objects.filter(subject_identifier=subject_identifier):
            update_log = UpdateLog.objects.get(subject_identifier=subject_identifier)
            update_log.update_datetime = datetime.today()
            update_log.save()
        else:
            UpdateLog.objects.create(subject_identifier=subject_identifier, update_datetime=datetime.today())

    def fetch(self, **kwargs):
        """
        Update and Fetch the local copy of lab data for a given set of labs.
        """
        subject_identifier = kwargs.get('subject_identifier')
        labs = kwargs.get('labs')
        self.update(subject_identifier=subject_identifier, labs=labs)
        # return filtered model instance
        return super(ResultManager, self).filter(lab__subject_identifier=subject_identifier)
