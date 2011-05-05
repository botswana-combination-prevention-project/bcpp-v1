
def fetch_lists_from_dmis(**kwargs):
    import datetime
    import pyodbc
    from bhp_lab_core.models import AliquotType, AliquotCondition,Panel, PanelGroup
    from bhp_lab_test_code.models import TestCode, TestCodeGroup, TestCodeReferenceList, TestCodeReferenceListItem
    from bhp_lab_core.models import DmisImportHistory

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

    #test_code_reference
    sql  = 'SELECT PID, UTESTID as test_code, LONGNAME, UTESTID_UNITS, \
            convert(decimal(12,4), LLN) as lln, \
            convert(decimal(12,4), ULN) as uln, \
            GENDER as gender, \
            age_low, age_low_unit,\
            age_low_quantifier, \
            age_high, age_high_unit,\
            age_high_quantifier, \
            convert(decimal(12,4), panic_value) as panic_value, \
            panic_value_quantifier \
            FROM BHPLAB.DBO.F0110ResponseReference \
            where age_low <> 0 and age_high<>120'
    cursor.execute(sql)

    #create a parent record for the TestCodeReferenceListItem(s) if it does not exist
    oTestCodeReferenceList = TestCodeReferenceList.objects.filter(name__iexact='BHPLAB_NORMAL_RANGES_201005')
    if not oTestCodeReferenceList:
        oTestCodeReferenceList = TestCodeReferenceList(
            name = 'BHPLAB_NORMAL_RANGES_201005',
            description = 'BHPLAB_NORMAL_RANGES_201005',
            )
        oTestCodeReferenceList.save()        
    else:
        oTestCodeReferenceList = TestCodeReferenceList.objects.get(name__iexact='BHPLAB_NORMAL_RANGES_201005')        

    TestCodeReferenceListItem.objects.all().delete()    
    
    for row in cursor:
        oTestCode = TestCode.objects.filter(code__iexact=row.test_code)

        if oTestCode:
            oTestCode = TestCode.objects.get(code__iexact=row.test_code)
            if row.panic_value:
                panic_value = ('%.4f' % (row.panic_value,))
            else:
                panic_value = None
                    
            TestCodeReferenceListItem.objects.create( 
                test_code_reference_list = oTestCodeReferenceList,
                test_code=oTestCode,
                gender = row.gender.upper(),
                uln = ('%.4f' % (row.uln,)),
                lln = ('%.4f' % (row.lln,)),
                age_low = row.age_low,
                age_low_unit = row.age_low_unit.upper(),
                age_low_quantifier = row.age_low_quantifier,
                age_high = row.age_high,
                age_high_unit = row.age_high_unit.upper() ,
                age_high_quantifier = row.age_high_quantifier,
                panic_value = panic_value,
                panic_value_quantifier = row.panic_value_quantifier,
                )
            
    #grading
    sql  = 'select PID_NAME as name, comment as description from bhpdmc.dbo.dm100response'
    
    sql = ''
    
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
    
    
if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/erikvw/source/')
    sys.path.append('/home/erikvw/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    print 'fetching lab lists....'
    fetch_lists_from_dmis()
    print 'Done'
    sys.exit (0)              
