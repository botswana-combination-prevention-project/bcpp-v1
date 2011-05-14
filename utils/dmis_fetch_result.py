"""
import results for orders already in the system
"""

def fetch_results_from_dmis(**kwargs):

    import pyodbc, datetime
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TestCode, AliquotMedium, AliquotType, AliquotCondition, TidPanelMapping, Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource
    from bhp_lab_core.models import DmisImportHistory, ResultSource
    from bhp_lab_core.utils import AllocateResultIdentifier
    
    #Result.objects.all().delete()

    oOrders  = Order.objects.all()
    
    for oOrder in oOrders:
        fetch_or_create_result(order=oOrder)

def fetch_or_create_result(**kwargs):

    import pyodbc, datetime, re
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TestCode, AliquotMedium, AliquotType, AliquotCondition, TidPanelMapping, Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource
    from bhp_lab_core.models import DmisImportHistory, ResultSource
    from bhp_lab_core.utils import AllocateResultIdentifier

    
    oOrder = kwargs.get('order')
        
    cnxn2 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor_result = cnxn2.cursor()

    cnxn3 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor_resultitem = cnxn3.cursor()

    if not Result.objects.filter(order=oOrder):
        sql ='select headerdate as result_datetime, \
              l21.keyopcreated as user_created, \
              l21.datecreated as created, \
              convert(varchar(36), l21.result_guid) as result_guid \
              from BHPLAB.DBO.LAB21Response as L21 \
              where l21.id=\'%s\' '  % oOrder.order_identifier
        
        cursor_result.execute(sql)
         
        for row in cursor_result:

            result_identifier=AllocateResultIdentifier(oOrder)    

            oResult = Result.objects.create(
                result_identifier=result_identifier,
                order = oOrder,
                result_datetime=row.result_datetime,
                comment='imported from dmis',
                user_created=row.user_created,
                created=row.created,
                dmis_result_guid=row.result_guid,
                )
                

            sql ='select l21d.sample_assay_date, \
                  utestid, \
                  result as result_value, \
                  result_quantifier, \
                  status, \
                  mid,\
                  l21d.validation_ref as validation_reference, \
                  l21d.datelastmodified as result_item_datetime, \
                  l21d.keyopcreated as user_created, \
                  l21.datecreated as created \
                  from BHPLAB.DBO.LAB21Response as L21 \
                  left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21.Q001X0=L21D.QID1X0 \
                  where l21.id=\'%s\' and l21d.id is not null'  % oResult.order.order_identifier
            
            cursor_resultitem.execute(sql)
            
            fetch_or_create_resultsource()
            
            for ritem in cursor_resultitem:
                test_code = ritem.utestid.strip(' \t\n\r')
                oTestCode=TestCode.objects.get(code__exact=test_code)
                # change NT system username to auto
                if ritem.user_created=='NT AUTHORITY\SYSTEM':
                    user_created='auto'
                else:
                    user_created=ritem.user_created
                # evaluate validation_reference
                if ritem.validation_reference == '-9':
                    # this is an item from GetResults TCP connected to PSM
                    result_item_source = fetch_or_create_resultsource(interface='psm_interface')                
                    result_item_source_reference = ''
                    validation_reference = 'dmis-auto'
                elif ritem.validation_reference == 'LAB21:MANUAL':
                    # manual entry and no validation -- straight to LAB21 tableset
                    result_item_source = fetch_or_create_resultsource(interface='manual_entry')                
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'auto'                
                elif re.search('^rad[0-9A-F]{5}\.tmp$', ritem.validation_reference):    
                    # this is an item from GetResults Flatfile and validated via the LAB05 path
                    result_item_source = fetch_or_create_resultsource(interface='cd4_interface')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'lab05'                               
                elif re.search('^LAB23:', ritem.validation_reference):          
                    # manual entry and validated via the LAB23 validation path                           
                    result_item_source = fetch_or_create_resultsource(interface='manual_entry')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'lab23'                               
                elif re.search('^IMPORT', ritem.validation_reference):          
                    # manual entry and validated via the LAB23 validation path                           
                    result_item_source = fetch_or_create_resultsource(interface='direct_import')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'auto'     
                elif re.search('^LB003:', ritem.validation_reference):          
                    # manual entry and validated via the LAB23 validation path                           
                    result_item_source = fetch_or_create_resultsource(interface='direct_import')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'auto'     
                elif re.search('^LB004:', ritem.validation_reference):          
                    # manual entry and validated via the LAB23 validation path                           
                    result_item_source = fetch_or_create_resultsource(interface='direct_import')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'auto'  
                elif re.search('^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$', ritem.validation_reference):                   
                    result_item_source = fetch_or_create_resultsource(interface='manual_entry')
                    result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                    validation_reference = 'auto'  
                else:
                    # missed a case? let's hear about it
                    raise TypeError('Validation reference \'%s\' was not expected. See dmis_fetch_result.' % ritem.validation_reference)

                # create a new result item. set validation to 'P', we'll import 
                # full validation information later 
                ResultItem.objects.create(
                    result=oResult,
                    test_code=oTestCode,
                    result_item_datetime=ritem.result_item_datetime,                
                    result_item_value=ritem.result_value,
                    result_item_quantifier=ritem.result_quantifier,
                    validation_status='P',
                    validation_reference=validation_reference,
                    result_item_source=result_item_source,
                    result_item_source_reference=ritem.mid,
                    result_item_operator=user_created,                
                    comment='',
                    )
                
                
                
    return None
    
def fetch_or_create_resultsource( **kwargs ):
    from bhp_lab_core.models import ResultSource
    from django.db.models import Avg, Max, Min, Count        

    interfaces = ['psm_interface', 'cd4_interface','auto', 'manual_entry', 'direct_import',]
    agg = ResultSource.objects.aggregate(Max('display_index'),)
    if agg:
        display_index = agg['display_index__max']
    else:
        display_index = 0    

    # populate if not already ...
    for interface in interfaces:
        if not ResultSource.objects.filter(name__iexact=interface):
            oResultSource=ResultSource.objects.create(
                name=interface,
                short_name=interface,                
                display_index=display_index+10,
                )
            oResultSource.save()  
    # create a new one if given argument and does not exist already
    if kwargs.get('interface'):        
        if not ResultSource.objects.filter(name__iexact=kwargs.get('interface')):
            oResultSource=ResultSource.objects.create(
                name=kwargs.get('interface'),
                short_name=kwargs.get('interface'),                
                display_index=display_index+11,
                )
            oResultSource.save()  
        else:
            oResultSource=ResultSource.objects.get(name__iexact=kwargs.get('interface'))                        
    else:
        oResultSource = None
            
    return oResultSource         

if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/erikvw/source/')
    sys.path.append('/home/erikvw/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    
    import pyodbc, datetime
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TestCode, AliquotMedium, AliquotType, AliquotCondition, TidPanelMapping, Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource
    from bhp_lab_core.models import DmisImportHistory, ResultSource
    from bhp_lab_core.utils import AllocateResultIdentifier

    
    print 'fetching lab results from dmis....'
    fetch_results_from_dmis()
    print 'Done'
    sys.exit (0)                  
