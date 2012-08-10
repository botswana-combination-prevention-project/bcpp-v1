#from datetime import datetime
#from django.db import models
#from django.conf import settings
#from lab_test_code.models import TestCode, TestCodeGroup
#from lab_result_item.models import ResultItem as LisResultItem
##from bhp_poll_mysql.poll_mysql import PollMySQL
#from lab_clinic_api.models import UpdateLog


#class ResultItemManager(models.Manager):

#    def connected(self):
#        host = settings.DATABASES['lab_api']['HOST']
#        if not host:
#            host = 'localhost'
#        port = settings.DATABASES['lab_api']['PORT']
#        if not port:
#            port = '3306'
#        poll = PollMySQL(host, int(port))
#        return poll.is_server_active()

#    def update(self, **kwargs):
#        """
#        Using the 'lab_api' DATABASE connection defined in settings,
#        update the local copy of lab data and return nothing.
#
#        From your code, call 'fetch' instead of 'update'
#        """
#        subject_identifier = kwargs.get('subject_identifier')
#        results = kwargs.get('results')
#        if self.connected():
#            for result in results:
#                # update local "ResultItem" for this result
#                lis_result_items = LisResultItem.objects.using('lab_api').filter(result__result_identifier=result.result_identifier)
#                for lis_result_item in lis_result_items:
#                    if super(ResultItemManager, self).filter(result=result,
#                                                             test_code__code=lis_result_item.test_code.code):
#                        # update existing result_item
#                        result_item = super(ResultItemManager, self).get(result=result,
#                                                                         test_code__code=lis_result_item.test_code.code)
#                        for fld in result_item._meta.fields:
#                            if fld.name in [field.name for field in lis_result_item._meta.fields if field.name != 'id' and field.name != 'result' and field.name != 'test_code']:
#                                setattr(result_item, fld.name, getattr(lis_result_item, fld.name))
#                            result_item.result = result
#                        result_item.save()
#                    else:
#                        # insert new result_item
#                        # get local test_code by code/name
#                        if TestCode.objects.filter(code=lis_result_item.test_code.code):
#                            test_code = TestCode.objects.get(code=lis_result_item.test_code.code)
#                        else:
#                            #add test_code to local listing if it does not exist
#
#                            if not TestCodeGroup.objects.filter(code=lis_result_item.test_code.test_code_group.code):
#                                test_code_group = TestCodeGroup.objects.create(code=lis_result_item.test_code.test_code_group.code, name=lis_result_item.test_code.test_code_group.name)
#                            else:
#                                test_code_group = TestCodeGroup.objects.get(code=lis_result_item.test_code.test_code_group.code)
#                            test_code = TestCode()
#                            for field in test_code.objects._meta.fields:
#                                if field.name != 'id' and field.name != 'test_code_group':
#                                    test_code.__dict__[field.name] = lis_result_item.__dict__[field.name]
#                            test_code.test_code_group = test_code_group
#                            test_code.save()
#                        # update
#                        result_item = super(ResultItemManager, self).__dict__['model']()
#                        for fld in super(ResultItemManager, self).__dict__['model']._meta.fields:
#                            if fld.name in [field.name for field in lis_result_item._meta.fields if field.name != 'id' and field.name != 'result' and field.name != 'test_code']:
#                                setattr(result_item, fld.name, getattr(lis_result_item, fld.name))
#                        result_item.result = result
#                        result_item.test_code = test_code
#                        result_item.save()
#            if UpdateLog.objects.filter(subject_identifier=subject_identifier):
#                update_log = UpdateLog.objects.get(subject_identifier=subject_identifier)
#                update_log.update_datetime = datetime.today()
#                update_log.save()
#            else:
#                UpdateLog.objects.create(subject_identifier=subject_identifier, update_datetime=datetime.today())
#
#    def fetch(self, **kwargs):
#        """
#        Update and Fetch the local copy of lab data for a given set of labs.
#        """
#        subject_identifier = kwargs.get('subject_identifier')
#        results = kwargs.get('results')
#        self.update(subject_identifier=subject_identifier, results=results)
#        return super(ResultItemManager, self).filter(result__lab__subject_identifier=subject_identifier)
