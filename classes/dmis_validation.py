import pyodbc, datetime
from django.db.models import Q
from lab_result.models import Result, ResultSource
from lab_result_item.models import ResultItem
from lab_test_code.models import TestCode


class DmisValidation(object):

    def __init__(self, debug=False):
        self.debug = debug

    def fetch(self, **kwargs):

        cnxn2 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
        cursor_result = cnxn2.cursor()

        #unvalidate everything
        #Result.objects.using(self.lab_db).all().update(validation_status='P', validation_datetime=None, validation_username=None)

        self.lab_db = kwargs.get('lab_db', 'default')    
        subject_identifier = kwargs.get('subject_identifier', None)
        
        cd4_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='cd4_interface')
        psm_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='psm_interface')
        direct_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='direct_import') 
        manual_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='manual_entry')                           
        
        qset=Q(validation_status__iexact='P')

        #if kwargs.get('result_identifier'):
        #    qset.add(Q(result__result_identifier__iexact=kwargs.get('result_identifier')), Q.AND)
        
        if subject_identifier:
            qset.add(Q(result__order__aliquot__receive__patient__subject_identifier__iexact=subject_identifier), Q.AND)

        result_items  = ResultItem.objects.using(self.lab_db).filter(qset)
        
        for result_item in result_items:
            result=result_item.result
            
            if result_item.result_item_source==psm_interface:
                #use lab21 information for PSM, Manual, Import
                result_item.result_item_operator=result.user_created.strip('BHP\\bhp\\')
                result_item.validation_status='F'   
                result_item.validation_datetime=result_item.result_item_datetime
                result_item.validation_username='auto'
                result_item.save()        
                print 'result %s %s test_code %s ON %s' % (result.result_identifier,result.result_datetime,result_item.test_code, result_item.result_item_source )
            elif result_item.result_item_source==direct_interface:
                #use lab21 information for Import
                result_item.result_item_operator=result.user_created.strip('BHP\\bhp\\')
                result_item.validation_status='F'
                result_item.validation_datetime=result_item.result_item_datetime
                result_item.validation_username='auto'
                result_item.save()                        
                print 'result %s %s test_code %s ON %s' % (result.result_identifier,result.result_datetime,result_item.test_code, result_item.result_item_source )            
            elif result_item.result_item_source==cd4_interface:
                #this returns only one record per result, only, so update all items as one
                # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"                
                sql = "select top 1 result_accepted_username as operator, \
                        result_accepted_username as validation_username, \
                        l5.result_accessed_date as validation_datetime, \
                        archive_filename+' ('+exp_filename+')' as result_item_source_reference \
                        from bhplab.dbo.lab05response as l5 \
                        left join bhplab.dbo.results_101 as r101 on l5.result_guid=r101.result_guid \
                        where result_accepted=1 and convert(varchar(36),l5.result_guid)='%s'" % result.dmis_result_guid 
                        
                cursor_result = cnxn2.cursor() 
                cursor_result.execute(sql)  
                #try:
                for row in cursor_result:        
                    result_item.result_item_operator=row.operator.strip('BHP\\bhp\\')
                    result_item.validation_status='F'
                    result_item.validation_datetime=row.validation_datetime
                    result_item.validation_username=row.validation_username.strip('BHP\\bhp\\')
                    result_item.save()                            
                print 'result %s %s test_code %s ON %s' % (result.result_identifier,result.result_datetime,result_item.test_code, result_item.result_item_source )                    
                #except:
                #    pass                    

            elif result_item.result_item_source==manual_interface and result_item.validation_reference.lower()<>'lab23':                
                #use lab21 information for PSM, Manual, Import
                result_item.result_item_operator=result.user_created.strip('BHP\\bhp\\')
                result_item.validation_status='F'   
                result_item.validation_datetime=result_item.result_item_datetime
                result_item.validation_username='auto'
                result_item.save()                        
                print 'result %s %s test_code %s ON %s' % (result.result_identifier,result.result_datetime,result_item.test_code, result_item.result_item_source )            
            elif result_item.result_item_source==manual_interface and result_item.validation_reference.lower()=='lab23':
                #this returns one record per result, only, so update all items as one
                sql = "select lower(L23.operator) as operator, \
                        lower(l23d.checkbatch_user) as validation_username, \
                        l23d.datelastmodified as validation_datetime, \
                        convert(varchar, l23.id) as validation_reference \
                        from bhplab.dbo.lab23response as l23 \
                        left join bhplab.dbo.lab23responseq001x0 as l23d on l23.q001x0=l23d.qid1x0 \
                        where result_accepted=1 and upper(ltrim(rtrim(utestid)))='%s' and convert(varchar(36),result_guid)='%s'" % ( result_item.test_code.code, result.dmis_result_guid)
                cursor_result = cnxn2.cursor() 
                cursor_result.execute(sql)           
                for row in cursor_result:  
                    result_item.result_item_operator=row.operator.strip('BHP\\bhp\\')
                    result_item.validation_reference=row.validation_reference
                    result_item.validation_status='F'
                    result_item.validation_datetime=row.validation_datetime
                    result_item.validation_username=row.validation_username.strip('BHP\\bhp\\')                        
                    result_item.save()                            
                print 'result %s %s test_code %s ON %s' % (result.result_identifier,result.result_datetime,result_item.test_code, result_item.result_item_source )                    
                        
            else:
                raise TypeError('Unknown case result_item_source in dmis_fetch_validation. Got \'%s\' from result %s.' % (result.resultitem.result_item_source, result) )
        
