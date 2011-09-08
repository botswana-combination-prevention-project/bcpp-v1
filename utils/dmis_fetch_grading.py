
def fetch_grading_from_dmis(**kwargs):
    import datetime
    import pyodbc
    from lab_test_code.models import TestCode, TestCodeGroup
    from lab_grading.models import GradingList, GradingListItem    


    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()

    now  = datetime.datetime.today()


    #grading
    sql = "SELECT upper(utestid) as test_code, \
            convert(decimal(12,4), range_min) as lln, \
            convert(decimal(12,4), range_max) as uln, \
           age_min as age_low, lower(substring(age_interval_min,1,1)) as age_low_unit, range_q_min as age_low_quantifier,\
           age_max as age_high, lower(substring(age_interval_max,1,1)) as age_high_unit, range_q_max as age_high_quantifier,\
           grade,\
           case hiv_status when 2 then 'NEG' when 1 then 'POS' else 'ANY' end as hiv_status, \
           range_scale as utestid_decimal \
           FROM bhpdmc.dbo.dm100response AS dm100 \
           LEFT join  bhpdmc.dbo.dm100responseQ001X0 AS dm100d ON dm100.q001x0=dm100d.qid1x0 \
           WHERE pid_name='DAIDS_2004' \
           and utestid is not null and ltrim(utestid)<>'' \
           order by utestid"
    cursor.execute(sql)
    
    #create a parent record for the GradingListItem(s) if it does not exist
    oGradingList = GradingList.objects.filter(name__iexact='DAIDS_2004')
    if not oGradingList:
        oGradingList = GradingList(
            name = 'DAIDS_2004',
            description = 'DAIDS_2004',
            )
        oGradingList.save()        
    else:
        oGradingList = GradingList.objects.get(name__iexact='DAIDS_2004')        

    GradingListItem.objects.all().delete()    
    
    for row in cursor:
        
        test_code = row.test_code.strip(' \t\n\r')

        oTestCode = TestCode.objects.filter(code__iexact=test_code)

        if oTestCode:
            oTestCode = TestCode.objects.get(code__iexact=test_code)
            panic_value = None
                    
            GradingListItem.objects.create( 
                grading_list = oGradingList,
                test_code=oTestCode,
                grade = row.grade,
                gender = 'MF',
                hiv_status = row.hiv_status,
                uln = ('%.4f' % (row.uln,)),
                lln = ('%.4f' % (row.lln,)),
                age_low = row.age_low,
                age_low_unit = row.age_low_unit.upper(),
                age_low_quantifier = row.age_low_quantifier,
                age_high = row.age_high,
                age_high_unit = row.age_high_unit.upper() ,
                age_high_quantifier = row.age_high_quantifier,
                panic_value_low = panic_value,
                panic_value_high = panic_value,                
                )
                
                
if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/erikvw/source/')
    sys.path.append('/home/erikvw/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    print 'fetching grading list....'
    fetch_grading_from_dmis()
    print 'Done'
    sys.exit (0)                
