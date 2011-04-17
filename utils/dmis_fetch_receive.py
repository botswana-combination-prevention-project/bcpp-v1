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
    
    #note that some records will not be imported for having>1
    sql  = 'select top 5000 min(l.id) as dmis_reference, \
            l.pid as receive_identifier, \
            l.sample_protocolnumber as protocol_identifier, \
            l.gender, \
            min(dob) as dob, \
            l.pat_id as subject_identifier, \
            l.pinitials as initials, \
            l.keyopcreated as user_created, \
            l.keyoplastmodified as user_modified, \
            min(l.headerdate) as datetime_received, \
            min(l.sample_date_drawn) as datetime_drawn, \
            min(l.datecreated) as created, \
            min(l.datelastmodified) as modified \
            from lab01response as l \
            left join lab21response as l21 on l.pid=l21.pid \
            where l21.pid is %s \
            and l.datelastmodified <= \'%s\' \
            and sample_date_drawn <= \'%s\' \
            group by l.pid, l.sample_protocolnumber, l.pat_id, l.gender, l.pinitials, l.keyopcreated, l.keyoplastmodified  \
            having count(*)=1 \
            order by min(l.id) desc' % (has_order_sql, import_datetime.strftime('%Y-%m-%d %H:%M'), now.strftime('%Y-%m-%d %H:%M'))

    #raise TypeError(sql)

    cursor.execute(sql)
     
    for row in cursor:

        oReceive = fetch_or_create_receive( 
            receive_identifier = row.receive_identifier,
            protocol_identifier = row.protocol_identifier,
            subject_identifier = row.subject_identifier,
            gender = row.gender,
            dob = row.dob,
            initials = row.initials,
            datetime_drawn = row.datetime_drawn,
            datetime_received = row.datetime_received,
            user_created = row.user_created,
            user_modified = row.user_modified,
            created = row.created,
            modified = row.modified,
            dmis_reference=row.dmis_reference,
            )
            
        oOrder = fetch_or_create_order( 
            order_identifier = row.receive_identifier,
            protocol_identifier = row.protocol_identifier,
            subject_identifier = row.subject_identifier,
            gender = row.gender,
            dob = row.dob,
            initials = row.initials,
            datetime_drawn = row.datetime_drawn,
            datetime_received = row.datetime_received,
            user_created = row.user_created,
            user_modified = row.user_modified,
            created = row.created,
            modified = row.modified,
            dmis_reference=row.dmis_reference,
            )
        
        #oResult = fetch_or_create_result()
        
                    
                               
    try:
        cursor.close()          
    except:
        pass
        
    return None        

def fetch_or_create_receive( **kwargs ):

    receive_identifier = kwargs.get('receive_identifier')
    protocol_identifier = kwargs.get('protocol_identifier')    
    subject_identifier = kwargs.get('subject_identifier')
    initials = kwargs.get('initials')
    gender = kwargs.get('gender')
    dob = kwargs.get('dob')
    datetime_drawn = kwargs.get('datetime_drawn')
    datetime_received = kwargs.get('datetime_received')
    user_created = kwargs.get('user_created')
    user_modified = kwargs.get('user_modified')    
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')                    

    oReceive = Receive.objects.filter(receive_identifier=receive_identifier)

    if oReceive:
        oReceive = Receive.objects.get(receive_identifier=receive_identifier)    
    else:
        oProtocol = fetch_or_create_protocol(protocol_identifier)
        oAccount = fetch_or_create_account(protocol_identifier)
        oPatient = fetch_or_create_patient(
                                    account = oAccount, 
                                    subject_identifier = subject_identifier, 
                                    gender=gender, 
                                    dob=dob, 
                                    initials=initials,
                                    )
        oReceive = Receive.objects.create(
            protocol = oProtocol,
            receive_identifier = receive_identifier,
            patient = oPatient,
            datetime_drawn = datetime_drawn,
            datetime_received = datetime_received,
            user_created = user_created,
            user_modified = user_modified,
            created = created,                                    
            modified = modified,  
            dmis_reference = dmis_reference,
            ) 
        #oReceive.save()


    return oReceive
    
def fetch_or_create_order( **kwargs ):

    receive_identifier = kwargs.get('receive_identifier')
    protocol_identifier = kwargs.get('protocol_identifier')    
    subject_identifier = kwargs.get('subject_identifier')
    initials = kwargs.get('initials')
    gender = kwargs.get('gender')
    dob = kwargs.get('dob')
    datetime_drawn = kwargs.get('datetime_drawn')
    datetime_received = kwargs.get('datetime_received')
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')                    
 
    oOrder = Order.objects.filter(receive_identifier = receive_identifier )
            
    if oOrder:
        oOrder = Receive.objects.get(receive_identifier = receive_identifier )    
    else:
        oProtocol = fetch_or_create_protocol(protocol_identifier)
        oAccount = fetch_or_create_account(protocol_identifier)
        oPatient = fetch_or_create_patient(
                                    account = oAccount, 
                                    subject_identifier = subject_identifier, 
                                    gender=gender, 
                                    dob=dob, 
                                    initials=initials,
                                    )
        oReceive = Receive(
            protocol = oProtocol,
            receive_identifier = receive_identifier,
            patient = oPatient,
            datetime_drawn = datetime_drawn,
            datetime_received = datetime_received,
            #user_created = row.keyopcreated,
            #user_modified = row.keyoplastmodified,
            created = created,                                    
            modified = modified,  
            dmis_reference = dmis_reference,
            ) 
        oReceive.save()

    return oReceive


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

    oPatient = Patient.objects.filter(subject_identifier__iexact=kwargs.get('subject_identifier'))
    
    if oPatient:
        oPatient = Patient.objects.get(subject_identifier__iexact=kwargs.get('subject_identifier'))
    else:
        initials = kwargs.get('initials')
        account = kwargs.get('account')
        if not initials:
            initials = 'X0X'
    
        oPatient = Patient.objects.create(
            subject_identifier = kwargs.get('subject_identifier'),
            initials = initials,
            gender = kwargs.get('gender'),
            dob = kwargs.get('dob'),
            is_dob_estimated = '-',
            comment = 'auto created / imported from DMIS',            
            )
        oPatient.account.add(account)        

    
    return oPatient    


