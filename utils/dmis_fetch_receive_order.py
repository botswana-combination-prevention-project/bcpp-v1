

def fetch_receive_from_dmis(process_status, **kwargs):
    import datetime
    import pyodbc
    from django.db.models import Avg, Max, Min, Count    
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory
    
    subject_identifier = kwargs.get('subject_identifier')
    receive_identifier = kwargs.get('receive_identifier')
    order_identifier = kwargs.get('order_identifier')    
    aliquot_identifier = kwargs.get('aliquot_identifier')

    #Order.objects.all().delete()
    #Aliquot.objects.all().delete()
    #Receive.objects.all().delete()

    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
    cursor = cnxn.cursor()

    now  = datetime.datetime.today()
    
    #insert new record into ImportHistory
    obj = DmisImportHistory.objects.create(
        import_label='fetch_receive'
        )
    import_datetime = obj.import_datetime
    
    if process_status == 'pending':
        has_order_sql = 'null'
    elif process_status == 'available':
        has_order_sql = 'not null'
    else:
        raise TypeError('process_status must be \'pending\' or \'available\'. You wrote %s' % process_status)    
    
    #note that some records will not be imported for having>1
    sql  = 'select top 20000 min(l.id) as dmis_reference, \
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
            l.keyopcreated as user_created, \
            l.keyoplastmodified as user_modified, \
            min(l.headerdate) as receive_datetime, \
            min(l.sample_date_drawn) as datetime_drawn, \
            min(l.datecreated) as created, \
            min(l.datelastmodified) as modified, \
            l21.id as order_identifier, \
            l21.panel_id \
            from lab01response as l \
            left join lab21response as l21 on l.pid=l21.pid \
            where l21.pid is %s \
            and l.datelastmodified <= \'%s\' \
            and sample_date_drawn <= \'%s\' \
            group by l.pid, l.tid, l.sample_condition, l.sample_site_id, l.sample_visitid ,l.sample_protocolnumber, l.pat_id, l.gender, l.pinitials, l.keyopcreated, l.keyoplastmodified, l21.id, l21.panel_id  \
            having count(*)=1 \
            order by min(l.id) desc' % (has_order_sql, import_datetime.strftime('%Y-%m-%d %H:%M'), now.strftime('%Y-%m-%d %H:%M'))

    #raise TypeError(sql)

    cursor.execute(sql)
     
    for row in cursor:
        oReceive = fetch_or_create_receive( 
            receive_identifier = row.receive_identifier,
            protocol_identifier = row.protocol_identifier,
            site_identifier = row.site_identifier,            
            visit = row.visit,
            subject_identifier = row.subject_identifier,
            gender = row.gender,
            dob = row.dob,
            initials = row.initials,
            datetime_drawn = row.datetime_drawn,
            receive_datetime = row.receive_datetime,
            user_created = row.user_created,
            user_modified = row.user_modified,
            created = row.created,
            modified = row.modified,
            dmis_reference=row.dmis_reference,
            )
            
        #create an aliquot record, will guess specimen type by tid    
        oAliquot = fetch_or_create_aliquot( receive=oReceive , condition=row.sample_condition, primary=True, tid=row.tid )
        
        if process_status == 'available':
            #get panel using TID or l21.panel_id
            if not row.panel_id == None and not row.panel_id == '-9':
                oPanel = Panel.objects.get(dmis_panel_identifier__exact=row.panel_id)
            else:                                
                oPanel = Panel.objects.filter(panel_group__name__exact=row.tid)[0]
            #create new order
            oOrder = fetch_or_create_order( 
                order_identifier = row.order_identifier,
                order_datetime = row.receive_datetime,
                aliquot = oAliquot,
                panel=oPanel,
                user_created = row.user_created,
                user_modified = row.user_modified,
                created = row.created,
                modified = row.modified,
                dmis_reference=row.dmis_reference,
                )
            
            #oResult = fetch_or_create_result(order=oOrder)
                               
    try:
        cursor.close()          
    except:
        pass
        
    return None        

def fetch_or_create_receive( **kwargs ):

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

    receive_identifier = kwargs.get('receive_identifier')
    protocol_identifier = kwargs.get('protocol_identifier')
    site_identifier = kwargs.get('site_identifier')    
    visit = kwargs.get('visit')    
    subject_identifier = kwargs.get('subject_identifier')
    initials = kwargs.get('initials')
    gender = kwargs.get('gender')
    dob = kwargs.get('dob')
    datetime_drawn = kwargs.get('datetime_drawn')
    receive_datetime = kwargs.get('receive_datetime')
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
        oSite = fetch_or_create_site(site_identifier)        
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
            site=oSite,
            visit=visit,
            datetime_drawn = datetime_drawn,
            receive_datetime = receive_datetime,
            user_created = user_created,
            user_modified = user_modified,
            created = created,                                    
            modified = modified,  
            dmis_reference = dmis_reference,
            ) 
        #oReceive.save()


    return oReceive
    
def fetch_or_create_order( **kwargs ):

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

    order_identifier = kwargs.get('order_identifier')
    oPanel = kwargs.get('panel')
    oAliquot = kwargs.get('aliquot')    
    order_datetime = kwargs.get('order_datetime')
    comment = '',
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')                    
 
    oOrder = Order.objects.filter(order_identifier = order_identifier )
            
    if oOrder:
        oOrder = Order.objects.get(order_identifier = order_identifier )    
    else:
        oOrder = Order(
            order_identifier = order_identifier,
            order_datetime = order_datetime,
            aliquot = oAliquot,
            panel = oPanel,
            comment = '',
            created = created,
            modified = modified,
            dmis_reference = dmis_reference,
            ) 
        oOrder.save()

    return oOrder

def fetch_or_create_site( site_identifier ):
    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

    if site_identifier == None or site_identifier == '' or site_identifier == '-9':
        site_identifier = '00'
        
    oSite = Site.objects.filter(site_identifier__iexact=site_identifier)

    if oSite:
        oSite = Site.objects.get(site_identifier__iexact=site_identifier)
    else:
        oLocation = Location.objects.filter(name__exact='UNKNOWN')
        if oLocation:
            oLocation = Location.objects.get(name__exact='UNKNOWN')        
        else:
            oLocation = Location(
                name = 'UNKNOWN',
                )
            oLocation.save()

        oSite = Site(
            site_identifier = site_identifier,
            name = site_identifier,
            location=oLocation,
            )
        oSite.save()
    return oSite        

def fetch_or_create_protocol( protocol_identifier ):

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

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

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

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

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

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


def fetch_or_create_aliquot( **kwargs ):
    
    import datetime
    import pyodbc
    from django.db.models import Avg, Max, Min, Count    
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium, Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

    oReceive = kwargs.get('receive')
    
    oCondition = fetch_or_create_aliquotcondition(kwargs.get('condition'))
    
    tid = kwargs.get('tid')

    #create primary
    create = {}
    if tid == '411':
        create['type'] = '02' #WB
        create['medium'] = 'DBS'
    else:
        create['type'] = '02' #WB
        create['medium'] = 'TUBE'
    
    aliquot_identifier = '%s0000%s01' % (oReceive.receive_identifier, create['type'])    
    
    oAliquot = Aliquot.objects.filter(aliquot_identifier__iexact=aliquot_identifier)
    
    if oAliquot:
        oAliquot = Aliquot.objects.get(aliquot_identifier__iexact=aliquot_identifier)
    else:
        create['comment'] = 'auto created on import from DMIS'
        oAliquotType = AliquotType.objects.get(numeric_code__exact=create['type'])
        oAliquotMedium = AliquotMedium.objects.get(short_name__iexact=create['medium'])            
        oAliquot = Aliquot.objects.create(
            aliquot_identifier = aliquot_identifier,
            receive = oReceive,
            count = 1,
            aliquot_type = oAliquotType,
            medium = oAliquotMedium,
            condition=oCondition,
            comment = create['comment'],            
            )
        #oAliquot.account.add(account)        

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
        aliquot_identifier = '%s0201%s02' % (oReceive.receive_identifier, create['type'])    
        create['comment'] = 'auto created on import from DMIS'
        oAliquot = Aliquot.objects.filter(aliquot_identifier__iexact=aliquot_identifier)
        if oAliquot:
            oAliquot = Aliquot.objects.get(aliquot_identifier__iexact=aliquot_identifier)
        else:
            oAliquotType = AliquotType.objects.get(numeric_code__exact=create['type'])
            oAliquotMedium = AliquotMedium.objects.get(short_name__iexact=create['medium'])   
            oCondition = AliquotCondition.objects.get(short_name__iexact=create['condition'])            
            oAliquot = Aliquot.objects.create(
                aliquot_identifier = aliquot_identifier,
                receive = oReceive,
                count = 2,
                aliquot_type = oAliquotType,
                medium = oAliquotMedium,
                condition=oCondition,
                comment = create['comment'],            
                )

    return oAliquot

def fetch_or_create_aliquotcondition( **kwargs ):

    import datetime
    import pyodbc
    from django.db.models import Avg, Max, Min, Count    
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,AliquotMedium, Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory

    if AliquotCondition.objects.filter(short_name__exact=kwargs.get('condition')):
        oCondition = AliquotCondition.objects.get(short_name__exact=kwargs.get('condition'))
    else:        
        display_index = AliquotCondition.objects.aggregate(Max('display_index'),)
        if not display_index:
            display_index = 10
        else:
            display_index = display_index + 10
                
        oCondition = AliquotCondition(
            name = kwargs.get('condition'),
            short_name = kwargs.get('condition'),
            display_index = display_index,
            )    
        oCondition.save()
        
    return oCondition        

if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/erikvw/source/')
    sys.path.append('/home/erikvw/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)

    import datetime
    import pyodbc
    from bhp_lab_core.models import Receive, Aliquot, Order, Result, ResultItem, TidPanelMapping
    from bhp_lab_core.models import AliquotType, AliquotCondition,Panel, PanelGroup
    from bhp_lab_registration.models import Patient, Account
    from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location
    from bhp_lab_core.models import DmisImportHistory
    
    print 'fetching lab receiving and orders from dmis....'
    print 'fetch pending....'
    fetch_receive_from_dmis('pending')
    print 'fetch available....'
    fetch_receive_from_dmis('available')    
    print 'Done'
    sys.exit (0)                  
