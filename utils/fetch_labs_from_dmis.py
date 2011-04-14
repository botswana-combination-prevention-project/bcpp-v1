import pyodbc
from bhp_lab_temptables.models import LabSimpleResult, LabError
from bhp_lab_core.models import TestCode, TestGroup


def fetch_labs_from_dmis():

    """
from bhp_lab_temptable.utils import fetch_labs_from_dmis
fetch_labs_from_dmis()
    """
    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()
    
    cursor.execute("select top 500 * from mochudi_labtemp where utestid is not null")
       
    LabSimpleResult.objects.all().delete()

    for row in cursor:
    
        try:
            utestid = TestCode.objects.get(code=row.utestid)
            
            obj = LabSimpleResult(
                subject_identifier=row.subject_identifier,
                initials=row.initials,
                dob=row.dob,
                sample_id=row.sample_id,
                date_sample_drawn=row.date_sample_drawn,
                test=row.test,
                received=row.received,
                created=row.created,
                modified=row.modified,
                user_created=row.user_created,
                user_modified=row.user_modified,
                utestid=utestid.code,
                result=row.result,
                result_quantifier=row.result_quantifier,
                import_date=row.import_date)
            obj.save()  
        except:
            obj = LabError(
                subject_identifier=row.subject_identifier,
                initials=row.initials,
                dob=row.dob,
                sample_id=row.sample_id,
                date_sample_drawn=row.date_sample_drawn,
                test=row.test,
                received=row.received,
                created=row.created,
                modified=row.modified,
                user_created=row.user_created,
                user_modified=row.user_modified,
                utestid=row.utestid,
                result=row.result,
                result_quantifier=row.result_quantifier,
                import_date=row.import_date)
            obj.save()            

    try:
        cursor.close()          
    except:
        pass
        
    return LabSimpleResult.objects.all().count()        

    
    


