import pyodbc, datetime
from django.db.models import Avg, Max, Min, Count
from lab_result.models import Result, ResultSource
from lab_result_item.models import ResultItem

class DmisRelease(object):

    def __init__(self, debug=False):
        self.debug = debug

    def release(self, **kwargs):

        self.lab_db = kwargs.get('lab_db', 'default')    
        subject_identifier = kwargs.get('subject_identifier', None)
   
        if Result.objects.using(self.lab_db).filter(order__aliquot__receive__patient__subject_identifier=subject_identifier):        
            # update NT AUTHORITY username to 'auto' for any result_item
            ResultItem.objects.using(self.lab_db).filter(result__order__aliquot__receive__patient__subject_identifier=subject_identifier,result_item_operator__icontains='AUTHORITY').update(result_item_operator='auto')
            #unrelease everything
            Result.objects.using(self.lab_db).filter(order__aliquot__receive__patient__subject_identifier=subject_identifier).update(release_status='NEW')       

        oResults = Result.objects.using(self.lab_db).filter(order__aliquot__receive__patient__subject_identifier=subject_identifier,release_status__exact='NEW')
        
        for oResult in oResults:
            #get max validation datetime
            aggr = ResultItem.objects.using(self.lab_db).filter(result=oResult, validation_status__exact='F',).aggregate(Max('validation_datetime'),)
            if aggr['validation_datetime__max']:
                validation_datetime = aggr['validation_datetime__max']
                #get validation_username for that validation_datetime
                validation_username = ResultItem.objects.using(self.lab_db).filter(result=oResult, validation_status__exact='F', validation_datetime__exact=validation_datetime)[0].validation_username        
                if validation_username == 'auto':
                    validation_username = unicode('smoyo')
                # update result    
                oResult.release_status = 'RELEASED'
                oResult.release_datetime = validation_datetime
                oResult.release_username = validation_username
                oResult.save()  
