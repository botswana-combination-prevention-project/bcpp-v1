import datetime
import pyodbc
from bhp_lab_core.models import AliquotType, AliquotCondition, TestCode, TestCodeGroup, Panel, PanelGroup
from bhp_lab_core.models import DmisImportHistory

def fetch_lists_from_dmis(**kwargs):

    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()

    now  = datetime.datetime.today()
    
    #insert new record into ImportHistory
    obj = DmisImportHistory.objects.create(
        import_label='fetch_lists'
        )
    import_datetime = obj.import_datetime
    
    import_datetime = obj.import_datetime

    #aliquot types (WB, PL, etc)    
    sql  = 'select id, substring(PID_name,1,50) as name, \
            upper(PID) as alpha_code, sample_pip_code as numeric_code,\
            keyopcreated as user_created,\
            keyoplastmodified as user_modified,\
            datecreated as created,\
            datelastmodified as modified \
            from BHPLAB.DBO.ST515Response'
    cursor.execute(sql)
    AliquotType.objects.all().delete()
    for row in cursor:
        AliquotType.objects.create( 
            name=row.name,
            alpha_code=row.alpha_code,
            numeric_code=row.numeric_code,
            dmis_reference=row.id
            )
            
    

    #panels
    sql  = 'select id, substring(PID_name,1,50) as name, \
            upper(PID) as alpha_code, sample_pip_code as numeric_code,\
            keyopcreated as user_created,\
            keyoplastmodified as user_modified,\
            datecreated as created,\
            datelastmodified as modified \
            from BHPLAB.DBO.ST515Response'

    #raise TypeError(sql)

    cursor.execute(sql)

    AliquotType.objects.all().delete()
     
    for row in cursor:

        AliquotType.objects.create( 
            name=row.name,
            alpha_code=row.alpha_code,
            numeric_code=row.numeric_code,
            dmis_reference=row.id
            )    

    #testcodegroups
    sql  = 'select tid FROM BHPLAB.DBO.F0110Response group by tid'
    cursor.execute(sql)
    TestCodeGroup.objects.all().delete()
    for row in cursor:
        TestCodeGroup.objects.create( 
            code=row.tid,
            )    

    #testcodes
    sql  = 'select utestid as code, substring(longname,1,50) as name, utestid_units as units, \
            utestid_dec as display_decimal_places, \
            range_low as reference_range_lo, \
            range_high as reference_range_hi, \
            lln, uln,\
            substring(UTESTID_valuetype,1,15) as is_absolute, \
            tid as test_code_group \
            FROM BHPLAB.DBO.F0110Response AS F0100'

    cursor.execute(sql)

    TestCode.objects.all().delete()
     
    for row in cursor:

        oTestCodeGroup = TestCodeGroup.objects.get(code__exact=row.test_code_group)

        TestCode.objects.create( 
            code=row.code,
            name=row.name,
            units=row.units,
            test_code_group=oTestCodeGroup,
            display_decimal_places=row.display_decimal_places,  
            reference_range_lo=row.reference_range_lo,
            reference_range_hi=row.reference_range_hi,  
            uln=row.uln,
            lln=row.lln,                                                                        
            is_absolute=row.is_absolute,
            )    

    #panelgroups
    sql  = 'select panel_group as panel_group \
            FROM BHPLAB.DBO.F0100Response \
            group by panel_group'
    cursor.execute(sql)
    PanelGroup.objects.all().delete()
    for row in cursor:
        PanelGroup.objects.create( 
            name=row.panel_group,
            )    

    #panels
    sql  = 'select substring(objname,1,50) as name, pid as dmis_panel_identifier, \
            panel_group as panel_group FROM BHPLAB.DBO.F0100Response \
            group by substring(objname,1,50), pid, panel_group'
            
    cursor.execute(sql)
    Panel.objects.all().delete()
    for row in cursor:
        oPanelGroup = PanelGroup.objects.get(name=row.panel_group)
        oPanel = Panel.objects.filter(name__iexact=row.name)
        if not oPanel:
            Panel.objects.create( 
                name=row.name,
                panel_group=oPanelGroup,
                dmis_panel_identifier=row.dmis_panel_identifier,
                )    
        

    try:
        cursor.close()          
    except:
        pass
    return None            
