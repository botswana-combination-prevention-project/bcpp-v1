import datetime
import pyodbc
from bhp_lab_core.models import Receive, Order, Result, ResultItem, TestCode, TestGroup
from bhp_lab_registration.models import Patient, Account
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource
from bhp_lab_core.models import DmisImportHistory


def fetch_receive_from_dmis(process_status, **kwargs):

    
    subject_identifier = kwargs.get('subject_identifier')
    receive_identifier = kwargs.get('receive_identifier')
    order_identifier = kwargs.get('order_identifier')    
    aliquot_identifier = kwargs.get('aliquot_identifier')

    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()

    now  = datetime.datetime.today()
    
    #insert new record into ImportHistory
    obj = DmisImportHistory()
    obj.save()
    
    import_datetime = obj.import_datetime
    
    if process_status == 'pending':
        has_order_sql = 'null'
    elif process_status == 'available':
        has_order_sql = 'not null'
    else:
        raise TypeError('process_status must be \'pending\' or \'available\'. You wrote %s' % process_status)    
    
    sql  = 'select top 500 min(l.id) as id, \
            l.pid as pid, \
            l.sample_protocolnumber, \
            l.gender, \
            min(dob) as dob, \
            l.pat_id, \
            min(l.headerdate) as headerdate, \
            min(l.sample_date_drawn) as sample_date_drawn, \
            min(l.datecreated) as datecreated, \
            min(l.datelastmodified) as datelastmodified \
            from lab01response as l \
            left join lab21response as l21 on l.pid=l21.pid \
            where l21.pid is %s \
            and l.datelastmodified <=\'%s\' \
            group by l.pid, l.sample_protocolnumber, l.pat_id, l.gender   \
            having count(*)=1 \
            order by l.id desc' % (has_order_sql, import_datetime.strftime('%Y-%m-%d %H:%M'))

    cursor.execute(sql)
     
    for row in cursor:
        
        oReceive = Receive.objects.filter(receive_identifier = row.pid)
        if not oReceive:
            oProtocol = fetch_or_create_protocol(row.sample_protocolnumber)
            oAccount = fetch_or_create_account(row.sample_protocolnumber)
            oPatient = fetch_or_create_patient(
                                        account = oAccount, 
                                        pat_id = row.pat_id, 
                                        gender=row.gender, 
                                        dob=row.dob, 
                                        initials='XX',
                                        )
            oReceive = Receive(
                protocol = oProtocol,
                receive_identifier = row.pid,
                patient = oPatient,
                datetime_drawn = row.sample_date_drawn,
                datetime_received = row.headerdate,
                #user_created = row.keyopcreated,
                #user_modified = row.keyoplastmodified,
                created = row.datecreated,                                    
                modified = row.datelastmodified,  
                dmis_reference = row.id,
                ) 
            oReceive.save()
                               
    try:
        cursor.close()          
    except:
        pass
        
    return None        

def fetch_or_create_protocol( protocol_identifier ):

    oProtocol = Protocol.objects.filter(protocol_identifier__iexact=protocol_identifier)
    
    if oProtocol:
        oProtocol = Protocol.objects.get(protocol_identifier__iexact=protocol_identifier)
    else:
        oPI = PrincipalInvestigator.objects.get(last_name='UNKNOWN')
        oSL = SiteLeader.objects.get(last_name='UNKNOWN')                
        oFS = FundingSource.objects.get(name='UNKNOWN')                

        oProtocol = Protocol(
            protocol_identifier = protocol_identifier,
            research_title = 'unknown',
            short_title = 'unknown',
            local_title = 'unknown',
            date_registered = datetime.datetime.today(),
            date_opened = datetime.datetime.today(),
            description = 'auto created / imported from DMIS',                        
            )
        oProtocol.save()
    
    return oProtocol    

def fetch_or_create_account( account_name ):

    oAccount = Account.objects.filter(account_name__iexact=account_name)
    
    if oAccount:
        oAccount = Account.objects.get(account_name__iexact=account_name)
    else:
        oAccount = Account(
            account_name = account_name,
            account_opendate = datetime.datetime.today(),
            account_closedate = datetime.datetime.today(),            
            user_created = 'auto',
            created = datetime.datetime.today(),                                    
            comment = 'auto created / imported from DMIS',            
            )
        oAccount.save()
    
    return oAccount    
    
def fetch_or_create_patient( **kwargs ):

    oPatient = Patient.objects.filter(subject_identifier__iexact=kwargs.get('pat_id'))
    
    if oPatient:
        oPatient = Patient.objects.get(subject_identifier__iexact=kwargs.get('pat_id'))
    else:
        initials = kwargs.get('initials')
        if not initials:
            initials = 'XX'
    
        oPatient = Patient(
            subject_identifier = kwargs.get('pat_id'),
            #account = kwargs.get('account'),
            initials = initials,
            gender = kwargs.get('gender'),
            dob = kwargs.get('dob'),
            is_dob_estimated = '',
            comment = 'auto created / imported from DMIS',            
            )
        oPatient.save()
    
    return oPatient    


