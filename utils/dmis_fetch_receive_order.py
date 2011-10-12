import sys,os
sys.path.append('/home/erikvw/source/')
sys.path.append('/home/erikvw/source/bhplab/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bhplab.settings'
from django.core.management import setup_environ
from bhplab import settings

setup_environ(settings)

from datetime import datetime, timedelta
import pyodbc
from django.db.models import Avg, Max, Min, Count    
from lab_receive.models import Receive
from lab_aliquot.models import Aliquot
from lab_aliquot_list.models import AliquotType, AliquotCondition,AliquotMedium
from lab_order.models import Order
from lab_result.models import Result
from lab_result_item.models import ResultItem
from lab_panel.models import Panel, PanelGroup, TidPanelMapping
from lab_patient.models import Patient
from lab_account.models import Account
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location


def fetch_receive_order(process_status, **kwargs):
    
    """Fetch receiving (lab01) and order (lab21) records from the mssql/vb version of dmis.
       
       Creates a new receive record, primary aliquot and order, if not exist.
       Needs work on determining the number of days since last import
       and which records to fetch (perhaps something older has been modeified.
       Also, call with both process_status (pending and available) to make sure you get everything.
    """

    subject_identifier = kwargs.get('subject_identifier')
    receive_identifier = kwargs.get('receive_identifier')
    order_identifier = kwargs.get('order_identifier')    
    aliquot_identifier = kwargs.get('aliquot_identifier')

    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()

    now  = datetime.today()
    
    #get last import_datetime
    #agg = DmisImportHistory.objects.aggregate(Max('import_datetime'),)    
    
    #last_import_datetime = agg['import_datetime__max']
    
    last_import_datetime = datetime.today() - timedelta(days=90)
    
    """
    #insert new record into ImportHistory
    obj = DmisImportHistory.objects.create(
        import_label='fetch_receive'
        )
    import_datetime = obj.import_datetime
    """
    import_datetime = datetime.today()
    
    if process_status == 'pending':
        has_order_sql = 'null'
    elif process_status == 'available':
        has_order_sql = 'not null'
    else:
        raise TypeError('process_status must be \'pending\' or \'available\'. You wrote %s' % process_status)    
    
    #note that some records will not be imported for having>1
    sql  = 'select min(l.id) as dmis_reference, \
            l.pid as receive_identifier, \
            l.tid, \
            l.sample_condition, \
            l.sample_site_id as site_identifier, \
            l.sample_visitid as visit, \
            l.sample_protocolnumber as protocol_identifier, \
            l.gender, \
            min(dob) as dob, \
            l.pat_id as subject_identifier, \
            l.pinitials as initials, \
            l.cinitials as clinician_initials, \
            l.keyopcreated as user_created, \
            l.keyoplastmodified as user_modified, \
            min(l.headerdate) as receive_datetime, \
            min(l.sample_date_drawn) as drawn_datetime, \
            min(l.datecreated) as created, \
            min(l.datelastmodified) as modified, \
            l21.id as order_identifier, \
            l21.panel_id \
            from lab01response as l \
            left join lab21response as l21 on l.pid=l21.pid \
            where l21.pid is %s \
            and l.datelastmodified >= \'%s\' \
            and l.datelastmodified <= \'%s\' \
            and sample_date_drawn <= \'%s\' \
            group by l.pid, l.tid, l.sample_condition, l.sample_site_id, l.sample_visitid ,l.sample_protocolnumber, l.pat_id, l.gender, l.pinitials, l.cinitials, l.keyopcreated, l.keyoplastmodified, l21.id, l21.panel_id  \
            having count(*)=1 \
            order by min(l.id) desc' % (has_order_sql, last_import_datetime.strftime('%Y-%m-%d %H:%M'), import_datetime.strftime('%Y-%m-%d %H:%M'), now.strftime('%Y-%m-%d %H:%M'))

    #raise TypeError(sql)

    cursor.execute(sql)
     
    for row in cursor:

        #get panel using TID or l21.panel_id
        if not row.panel_id == None and not row.panel_id == '-9':
            panel = Panel.objects.get(dmis_panel_identifier__exact=row.panel_id)
        else:
            panel = Panel.objects.filter(panel_group__name__exact=row.tid)
            if not panel:
                panel_group = PanelGroup.objects.create(name = row.tid,)
                panel = Panel.objects.create(
                                        name = row.tid,
                                        panel_group = panel_group,
                                        comment = 'temp',
                                        #dmis_panel_identifier = row.dmis_panel_identifier,
                                        #test_code = row.test_code,
                                        #aliquot_type = row.aliquot_type,
                                        #account = row.account,
                                        )
            else:
                panel = panel[0]    


        receive = create_or_update_receive( 
            receive_identifier = row.receive_identifier,
            protocol_identifier = row.protocol_identifier,
            site_identifier = row.site_identifier,            
            visit = row.visit,
            subject_identifier = row.subject_identifier,
            gender = row.gender,
            dob = row.dob,
            initials = row.initials,
            drawn_datetime = row.drawn_datetime,
            receive_datetime = row.receive_datetime,
            user_created = row.user_created,
            user_modified = row.user_modified,
            created = row.created,
            modified = row.modified,
            dmis_reference=row.dmis_reference,
            clinician_initials = row.clinician_initials,
            dmis_panel_name = panel.name,
            receive_condition = row.sample_condition,
            )
        #create an aliquot record, will guess specimen type by tid    
        aliquot = create_or_update_aliquot( receive=receive , condition=row.sample_condition, primary=True, tid=row.tid, modified=row.modified )
        
        if process_status == 'available':
            #create new order
            order = fetch_or_create_order( 
                order_identifier = row.order_identifier,
                order_datetime = row.receive_datetime,
                aliquot = aliquot,
                panel = panel,
                user_created = row.user_created,
                user_modified = row.user_modified,
                created = row.created,
                modified = row.modified,
                dmis_reference=row.dmis_reference,
                )
            
            #oResult = fetch_or_create_result(order=order)
                               
    try:
        cursor.close()          
    except:
        pass
        
    return None        

def create_or_update_receive( **kwargs ):

    receive_identifier = kwargs.get('receive_identifier').strip(' \t\n\r')
    protocol_identifier = kwargs.get('protocol_identifier').strip(' \t\n\r')
    site_identifier = kwargs.get('site_identifier').strip(' \t\n\r')    
    visit = kwargs.get('visit')    
    subject_identifier = kwargs.get('subject_identifier').strip(' \t\n\r')
    initials = kwargs.get('initials')
    gender = kwargs.get('gender')
    dob = kwargs.get('dob')
    drawn_datetime = kwargs.get('drawn_datetime')
    receive_datetime = kwargs.get('receive_datetime')
    user_created = kwargs.get('user_created')
    user_modified = kwargs.get('user_modified')    
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')        
    clinician_initials = kwargs.get('clinician_initials')
    dmis_panel_name = kwargs.get('dmis_panel_name')
    receive_condition = kwargs.get('receive_condition')


    receive = Receive.objects.filter(receive_identifier=receive_identifier)

    if receive:
        receive = Receive.objects.get(receive_identifier=receive_identifier)
        if not receive.modified == modified:
            print 'updating receive %s' % receive_identifier
            protocol = fetch_or_create_protocol(protocol_identifier)        
            site = fetch_or_create_site(site_identifier)                    
            receive.modified = modified
            receive.user_modified = user_modified
            receive.protocol = protocol
            receive.drawn_datetime = drawn_datetime
            receive.receive_datetime = receive_datetime
            receive.site = site
            receive.visit = visit
            receive.clinician_initials = clinician_initials
            receive.dmis_reference = dmis_reference
            receive.dmis_panel_name = dmis_panel_name
            receive.receive_condition = receive_condition
            
            receive.save()
    else:
        protocol = fetch_or_create_protocol(protocol_identifier)
        account = fetch_or_create_account(protocol_identifier)
        site = fetch_or_create_site(site_identifier)        
        patient = create_or_update_patient(
                                    account = account, 
                                    subject_identifier = subject_identifier, 
                                    gender=gender, 
                                    dob=dob, 
                                    initials=initials,
                                    )
        receive = Receive.objects.create(
            protocol = protocol,
            receive_identifier = receive_identifier,
            patient = patient,
            site = site,
            visit = visit,
            drawn_datetime = drawn_datetime,
            receive_datetime = receive_datetime,
            user_created = user_created,
            user_modified = user_modified,
            created = created,                                    
            modified = modified,  
            dmis_reference = dmis_reference,
            clinician_initials = clinician_initials,            
            dmis_panel_name = dmis_panel_name,
            receive_condition = receive_condition,
            ) 
        receive.save()
        print 'receive created for sample '+receive_identifier+' protocol '+ protocol_identifier


    return receive
    
def fetch_or_create_order( **kwargs ):

    order_identifier = kwargs.get('order_identifier')
    panel = kwargs.get('panel')
    aliquot = kwargs.get('aliquot')    
    order_datetime = kwargs.get('order_datetime')
    comment = '',
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')                    
 
    order = Order.objects.filter(order_identifier = order_identifier )
            
    if order:
        order = Order.objects.get(order_identifier = order_identifier )    
    else:
        order = Order(
            order_identifier = order_identifier,
            order_datetime = order_datetime,
            aliquot = aliquot,
            panel = panel,
            comment = '',
            created = created,
            modified = modified,
            dmis_reference = dmis_reference,
            ) 
        order.save()

    return order

def fetch_or_create_site( site_identifier ):

    if site_identifier == None or site_identifier == '' or site_identifier == '-9':
        site_identifier = '00'
        
    site = Site.objects.filter(site_identifier__iexact=site_identifier)

    if site:
        site = Site.objects.get(site_identifier__iexact=site_identifier)
    else:
        oLocation = Location.objects.filter(name__exact='UNKNOWN')
        if oLocation:
            oLocation = Location.objects.get(name__exact='UNKNOWN')        
        else:
            oLocation = Location(
                name = 'UNKNOWN',
                )
            oLocation.save()

        site = Site(
            site_identifier = site_identifier,
            name = site_identifier,
            location=oLocation,
            )
        site.save()
    return site        

def fetch_or_create_protocol( protocol_identifier ):

    protocol = Protocol.objects.filter(protocol_identifier__iexact=protocol_identifier)
    
    if protocol:
        protocol = Protocol.objects.get(protocol_identifier__iexact=protocol_identifier)
    else:
        oPI = PrincipalInvestigator.objects.get(last_name='UNKNOWN')
        oSL = SiteLeader.objects.get(last_name='UNKNOWN')                
        oFS = FundingSource.objects.get(name='UNKNOWN')                

        protocol = Protocol(
            protocol_identifier = protocol_identifier,
            research_title = 'unknown',
            short_title = 'unknown',
            local_title = 'unknown',
            date_registered = datetime.datetime.today(),
            date_opened = datetime.datetime.today(),
            description = 'auto created / imported from DMIS',                        
            )
        protocol.save()
    
    return protocol    

def fetch_or_create_account( account_name ):

    account = Account.objects.filter(account_name__iexact=account_name)
    
    if account:
        account = Account.objects.get(account_name__iexact=account_name)
    else:
        account = Account(
            account_name = account_name,
            account_opendate = datetime.datetime.today(),
            account_closedate = datetime.datetime.today(),            
            user_created = 'auto',
            created = datetime.datetime.today(),                                    
            comment = 'auto created / imported from DMIS',            
            )
        account.save()

    return account    
    
def create_or_update_patient( **kwargs ):

    subject_identifier = kwargs.get('subject_identifier').strip(' \t\n\r')
    initials = kwargs.get('initials').strip(' \t\n\r')
    if not initials:
        initials = 'X0X'
    account = kwargs.get('account')
    gender = kwargs.get('gender')
    dob = kwargs.get('dob')
    is_dob_estimated = '-'

    patient = Patient.objects.filter(subject_identifier__iexact=subject_identifier)
    if patient:
        patient = Patient.objects.get(subject_identifier__iexact=subject_identifier)
        patient.dob = dob
        patient.gender = gender
        patient.is_dob_estimated = is_dob_estimated
        patient.initials = initials
        patient.save()
    else:
        patient = Patient.objects.create(
            subject_identifier = subject_identifier,
            initials = initials,
            gender = gender,
            dob = dob,
            is_dob_estimated = is_dob_estimated,
            comment = 'auto created / imported from DMIS',            
            )
        patient.account.add(account)        
    return patient    


def create_or_update_aliquot( **kwargs ):

    receive = kwargs.get('receive')
    condition = kwargs.get('condition')
    tid = kwargs.get('tid')
    modified = kwargs.get('modified')    
    
    aliquot_condition = create_or_update_aliquotcondition( condition=condition )

    #create primary
    create = {}
    if tid == '411':
        create['type'] = '02' #WB
        create['medium'] = 'DBS'
    else:
        create['type'] = '02' #WB
        create['medium'] = 'TUBE'
    
    aliquot_identifier = '%s0000%s01' % (receive.receive_identifier, create['type'])    
    
    aliquot = Aliquot.objects.filter(aliquot_identifier__iexact=aliquot_identifier)
    
    if aliquot:
        aliquot = Aliquot.objects.get(aliquot_identifier__iexact=aliquot_identifier)
        if not aliquot.modified == modified:        
            aliquot_type = AliquotType.objects.get(numeric_code__exact=create['type'])        
            aliquot.modified = modified
            aliquot.aliquot_type = aliquot_type
            aliquot.condition = aliquot_condition
            aliquot.save()
        
    else:
        create['comment'] = 'auto created on import from DMIS'
        aliquot_type = AliquotType.objects.get(numeric_code__exact=create['type'])
        oAliquotMedium = AliquotMedium.objects.get(short_name__iexact=create['medium'])            
        aliquot = Aliquot.objects.create(
            aliquot_identifier = aliquot_identifier,
            receive = receive,
            count = 1,
            aliquot_type = aliquot_type,
            medium = oAliquotMedium,
            condition = aliquot_condition,
            comment = create['comment'],            
            )
        #aliquot.account.add(account)        

    #if order is not placed against primary, create child
    if tid[0]=='1':
        create = {}
    elif tid[0]=='2':    
        create['type'] = '06' #WB
        create['medium'] = 'TUBE'
        create['condition'] = '10'                
    elif tid[0]=='3':    
        create = {}
    elif tid[0]=='4':    
        create['type'] = '32' #WB
        create['medium'] = 'TUBE'
        create['condition'] = '10'        
    else:
        create = {}        


    if create:
        aliquot_identifier = '%s0201%s02' % (receive.receive_identifier, create['type'])    
        create['comment'] = 'auto created on import from DMIS'
        aliquot = Aliquot.objects.filter(aliquot_identifier__iexact=aliquot_identifier)
        if aliquot:
            aliquot = Aliquot.objects.get(aliquot_identifier__iexact=aliquot_identifier)
        else:
            aliquot_type = AliquotType.objects.get(numeric_code__exact=create['type'])
            oAliquotMedium = AliquotMedium.objects.get(short_name__iexact=create['medium'])   
            aliquot_condition = AliquotCondition.objects.get(short_name__iexact=create['condition'])            
            aliquot = Aliquot.objects.create(
                aliquot_identifier = aliquot_identifier,
                receive = receive,
                count = 2,
                aliquot_type = aliquot_type,
                medium = oAliquotMedium,
                condition=aliquot_condition,
                comment = create['comment'],            
                )

    return aliquot

def create_or_update_aliquotcondition( **kwargs ):

    if AliquotCondition.objects.filter(short_name__exact=kwargs.get('condition')):
        aliquot_condition = AliquotCondition.objects.get(short_name__exact=kwargs.get('condition'))
    else:        
        agg = AliquotCondition.objects.aggregate(Max('display_index'),)
        if not agg:
            display_index = 10
        else:
            display_index = agg['display_index__max'] + 10
                
        aliquot_condition = AliquotCondition(
            name = kwargs.get('condition'),
            short_name = kwargs.get('condition'),
            display_index = display_index,
            )    
        aliquot_condition.save()
        
    return aliquot_condition        

if __name__ == "__main__":
    
    print 'fetching lab receiving and orders from dmis....'
    print 'fetch pending....'
    fetch_receive_order('pending')
    print 'fetch available....'
    fetch_receive_order('available')    
    print 'Done'
    sys.exit (0)                  
