def fetch_validation_from_dmis(**kwargs):

    import pyodbc, datetime
    from django.db.models import Q
    from bhp_lab_core.models import TestCode, Result, ResultItem, ResultSource


    cnxn2 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor_result = cnxn2.cursor()

    #unvalidate everything
    #Result.objects.all().update(validation_status='P', validation_datetime=None, validation_username=None)

    oCD4_interface = ResultSource.objects.get(name__iexact='cd4_interface')
    oPSM_interface = ResultSource.objects.get(name__iexact='psm_interface')
    oDirect_interface = ResultSource.objects.get(name__iexact='direct_import') 
    oManual_interface = ResultSource.objects.get(name__iexact='manual_entry')                           

    oResults  = Result.objects.all()
    
    for oResult in oResults:
        if oResult.result_item_source==oPSM_interface:
            #use lab21 information for PSM, Manual, Import
            ResultItem.objects.filter(result=oResult).update(
                result_item_operator=oResult.user_created.strip('BHP\\bhp\\'),            
                validation_status='F',                        
                validation_datetime=oResult.result_datetime,
                validation_username='auto',
                )
        elif oResult.result_item_source==oDirect_interface:
            #use lab21 information for Import
            ResultItem.objects.filter(result=oResult).update(
                result_item_operator=oResult.user_created.strip('BHP\\bhp\\'),            
                validation_status='F',                        
                validation_datetime=oResult.result_datetime,
                validation_username='auto',
                )
        elif oResult.result_item_source==oCD4_interface:
            #this returns only one record per result, only, so update all items as one
            # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"                
            sql = "select top 1 result_accepted_username as operator, \
                    result_accepted_username as validation_username, \
                    l5.result_accessed_date as validation_datetime, \
                    archive_filename+' ('+exp_filename+')' as result_item_source_reference \
                    from bhplab.dbo.lab05response as l5 \
                    left join bhplab.dbo.results_101 as r101 on l5.result_guid=r101.result_guid \
                    where result_accepted=1 and l5.result_guid='%'" % oResult.dmis_result_guid 
                    
            cursor_result = cnxn2.cursor()        
            for row in cursor_result:        
                ResultItem.objects.filter(result=oResult).update(
                    result_item_operator=row.operator.strip('BHP\\bhp\\'),
                    validation_status='F',  
                    validation_datetime=row.validation_datetime,
                    validation_username=row.validation_username.strip('BHP\\bhp\\'),
                    )

        elif oResult.result_item_source==oManual_interface and oResult.result_item.validation_reference.lower()<>'lab23':                
            #use lab21 information for PSM, Manual, Import
            ResultItem.objects.filter(result=oResult).update(
                result_item_operator=oResult.user_created.strip('BHP\\bhp\\'),            
                validation_status='F',                        
                validation_datetime=oResult.result_datetime,
                validation_username='auto',
                )
        elif oResult.result_item_source==oManual_interface and oResult.result_item.validation_reference.lower()=='lab23':
            #this returns one record per result, only, so update all items as one
            sql = "select upper(ltrim(rtrim(utestid))) as test_code, \
                    lower(L23.operator) as operator, \
                    lower(l23d.checkbatch_user) as validation_username, \
                    l23d.datelastmodified as validation_datetime, \
                    convert(varchar, l23.id) as validation_reference \
                    from bhplab.dbo.lab23response as l23 \
                    left join bhplab.dbo.lab23responseq001x0 as l23d on l23.q001x0=l23d.qid1x0 \
                    where result_accepted=1 and result_guid='%'" % oResult.dmis_result_guid

            cursor_result = cnxn2.cursor()            
            for row in cursor_result:  
                oTestCode = TestCode.objects.get(code__exact=row.test_code)              
                ResultItem.objects.filter(result=oResult, test_code=oTestCode).update(
                    result_item_operator=row.operator.strip('BHP\\bhp\\'),
                    validation_reference=row.validation_reference,
                    validation_status='F',
                    validation_datetime=row.validation_datetime,
                    validation_username=row.validation_username.strip('BHP\\bhp\\')                        
                    )
        else:
            raise TypeError('Unknown case result_item_source in dmis_fetch_validation. Got \'%s\' from result %s.' % (oResult.resultitem.result_item_source, oResult) )
    
if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/django/source/')
    sys.path.append('/home/django/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    
    import pyodbc, datetime
    from bhp_lab_core.models import TestCode, Result, ResultItem

    print 'fetching lab results validation information from dmis....'
    fetch_validation_from_dmis()
    print 'Done'
    sys.exit (0)                  
