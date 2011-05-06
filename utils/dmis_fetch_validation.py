

def fetch_validation_from_dmis(**kwargs):

    import pyodbc, datetime
    from bhp_lab_core.models import TestCode, Result, ResultItem


    cnxn2 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor_result = cnxn2.cursor()

    #unvalidate everything
    #Result.objects.all().update(validation_status='P', validation_datetime=None, validation_username=None)

    oResults  = Result.objects.all()
    
    for oResult in oResults:
        
        #if oResult.validation_reference == '-9': 
        #    validation_reference='auto'
        #else:    
        #    validation_reference = oResult.validation_reference.lower()
        
        if validation_reference == 'auto':
            #use lab21 information
            ResultItem.objects.filter(result=oResult).update(
                validation_reference=validation_reference,
                validation_status='F',                        
                validation_datetime=oResult.result_datetime,
                validation_username=oResult.user_created,
                )
                                    
        else:    
            #use either LAB23 or LAB05
            #if order panel is CD4 get LAB05, otherwise LAB23
            if oResult.order.panel.name == 'CD4 (ARV)':
                #this returns only one record per result, only, so update all items as one
                # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"                
                sql = "select top 1 result_accepted_username as operator, \
                        result_accepted_username as validation_username, \
                        min(l5.result_accessed_date) as validation_datetime, \
                        case result_accepted when 1 then 'F' when 2 then 'R' else 'P' end as validation_status \
                        from bhplab.dbo.lab05response as l5 \
                        left join bhplab.dbo.results_101 as r101 on l5.result_guid=r101.result_guid \
                        where result_accepted=1 and [sample id]='%s' \
                        and archive_filename='{$arrRow['validation_method_ref']}' \
                        group by result_accepted_username" % (oResult.order.aliquot.receive.receive_identifier.upper())
                        
                cursor_result = cnxn2.cursor()        
                for row in cursor_result:                
                    ResultItem.objects.filter(result=oResult).update(
                        validation_reference=validation_reference,
                        validation_status=validation_status,                        
                        validation_datetime=row.validation_datetime,
                        validation_username=row.validation_username                        
                        )
                
            elif re.match(r'From\s+', 'Fromage amk')
:
                #this returns one record per result, only, so update all items as one
                # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"
                sql = "select upper(l23d.utestid) as test_code, \
                        lower(L23.operator) as operator, \
                        lower(l23d.checkbatch_user) as validation_username, \
                        l23d.datelastmodified as validation_datetime, \
                        case result_accepted when 1 then 'F' when 2 then 'R' else 'P' end as validation_status \
                        from bhplab.dbo.lab23response as l23 \
                        left join bhplab.dbo.lab23responseq001x0 as l23d on l23.q001x0=l23d.qid1x0 \
                        where l23d.BHHRL_REF='%s' and result_accepted=1 \
                        order by l23d.datelastmodified" % oResult.order.aliquot.receive.receive_identifier.upper()
                cursor_result = cnxn2.cursor()            
                for row in cursor_result:  
                    oTestCode = TestCode.objects.get(code__exact=row.test_code)              
                    ResultItem.objects.filter(result=oResult, test_code=oTestCode).update(
                        validation_reference=validation_reference,
                        validation_status=row.validation_status,
                        validation_datetime=row.validation_datetime,
                        validation_username=row.validation_username                        
                        )


    
if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/erikvw/source/')
    sys.path.append('/home/erikvw/source/bhplab/')
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
