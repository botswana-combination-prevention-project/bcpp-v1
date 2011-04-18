import datetime
import pyodbc
from bhp_lab_core.models import AliquotType, AliquotCondition, TestCode, TestGroup
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
    
    #note that some records will not be imported for having>1
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
            
    try:
        cursor.close()          
    except:
        pass
        
    return None            
