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

    oResultItems  = ResultItem.objects.all()
    
    for oResultItem in oResultItems:
        oResult=oResultItem.result
        if oResultItem.result_item_source==oPSM_interface:
            #use lab21 information for PSM, Manual, Import
            oResultItem.result_item_operator=oResult.user_created.strip('BHP\\bhp\\')
            oResultItem.validation_status='F'   
            oResultItem.validation_datetime=oResult.result_datetime
            oResultItem.validation_username='auto'
            oResultItem.save()        
        elif oResultItem.result_item_source==oDirect_interface:
            #use lab21 information for Import
            oResultItem.result_item_operator=oResult.user_created.strip('BHP\\bhp\\')
            oResultItem.validation_status='F'
            oResultItem.validation_datetime=oResult.result_datetime
            oResultItem.validation_username='auto'
            oResultItem.save()                        
        elif oResultItem.result_item_source==oCD4_interface:
            #this returns only one record per result, only, so update all items as one
            # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"                
            sql = "select top 1 result_accepted_username as operator, \
                    result_accepted_username as validation_username, \
                    l5.result_accessed_date as validation_datetime, \
                    archive_filename+' ('+exp_filename+')' as result_item_source_reference \
                    from bhplab.dbo.lab05response as l5 \
                    left join bhplab.dbo.results_101 as r101 on l5.result_guid=r101.result_guid \
                    where result_accepted=1 and convert(varchar(36),l5.result_guid)='%s'" % oResult.dmis_result_guid 
                    
            cursor_result = cnxn2.cursor()  
            raise TypeError(cursor_result)      
            for row in cursor_result:        
                oResultItem.result_item_operator=row.operator.strip('BHP\\bhp\\')
                oResultItem.validation_status='F'
                oResultItem.validation_datetime=row.validation_datetime
                oResultItem.validation_username=row.validation_username.strip('BHP\\bhp\\')
                oResultItem.save()                            

        elif oResultItem.result_item_source==oManual_interface and oResultItem.validation_reference.lower()<>'lab23':                
            #use lab21 information for PSM, Manual, Import
            oResultItem.result_item_operator=oResult.user_created.strip('BHP\\bhp\\')
            oResultItem.validation_status='F'   
            oResultItem.validation_datetime=oResult.result_datetime
            oResultItem.validation_username='auto'
            oResultItem.save()                        
        elif oResultItem.result_item_source==oManual_interface and oResultItem.validation_reference.lower()=='lab23':
            #this returns one record per result, only, so update all items as one
            sql = "select lower(L23.operator) as operator, \
                    lower(l23d.checkbatch_user) as validation_username, \
                    l23d.datelastmodified as validation_datetime, \
                    convert(varchar, l23.id) as validation_reference \
                    from bhplab.dbo.lab23response as l23 \
                    left join bhplab.dbo.lab23responseq001x0 as l23d on l23.q001x0=l23d.qid1x0 \
                    where result_accepted=1 and upper(ltrim(rtrim(utestid)))='%s' and convert(varchar(36),result_guid)='%s'" % ( oResult.test_code__code, oResult.dmis_result_guid)

            cursor_result = cnxn2.cursor()            
            for row in cursor_result:  
                oResultItem.result_item_operator=row.operator.strip('BHP\\bhp\\'),
                oResultItem.validation_reference=row.validation_reference,
                oResultItem.validation_status='F',
                oResultItem.validation_datetime=row.validation_datetime,
                oResultItem.validation_username=row.validation_username.strip('BHP\\bhp\\')                        
                oResultItem.save()                            
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
