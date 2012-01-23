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


class DmisReceive(object):

    def __init__(self, debug=False):
        self.debug = debug

    def fetch_receive(self, **kwargs):
        
        """Fetch receiving (lab01) and order (lab21) records from the mssql/vb version of dmis.
           
           Creates a new receive record, primary aliquot and order, if not exist.
           Needs work on determining the number of days since last import
           and which records to fetch (perhaps something older has been modeified.
           Also, call with both process_status (pending and available) to make sure you get everything.
        """
        lab_db = kwargs.get('lab_db', 'default')
        subject_identifier = kwargs.get('subject_identifier')

        if subject_identifier:
            where_subject_identifier = 'and l.pat_id like \'%'+subject_identifier+'%\'' 
            if self.debug:            
                print where_subject_identifier
        else:
            where_subject_identifier = ''
            
        receive_identifier = kwargs.get('receive_identifier')
        order_identifier = kwargs.get('order_identifier')    
        aliquot_identifier = kwargs.get('aliquot_identifier')

        cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
        cursor = cnxn.cursor()

        now  = datetime.today()
        import_tdelta = None
        days = kwargs.get("days")
        if days:
            try:
                import_tdelta = int(days)
            except:
                import_tdelta = None
        if import_tdelta:
            last_import_datetime = now - timedelta(days=import_tdelta)        
        else:        
            last_import_datetime = now - timedelta(days=7)
        import_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 23, 59)

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
    where l.datelastmodified >= \'%s\' \
    and l.datelastmodified <= \'%s\' \
    and sample_date_drawn <= \'%s\' \
    %s\
    group by l.pid, l.tid, l.sample_condition, l.sample_site_id, l.sample_visitid ,l.sample_protocolnumber, l.pat_id, l.gender, l.pinitials, l.cinitials, l.keyopcreated, l.keyoplastmodified, l21.id, l21.panel_id  \
    having count(*)=1 \
    order by min(l.id) desc' % (last_import_datetime.strftime('%Y-%m-%d %H:%M'), import_datetime.strftime('%Y-%m-%d %H:%M'), now.strftime('%Y-%m-%d %H:%M'), where_subject_identifier)

        cursor.execute(str(sql))
         
        for row in cursor:
            #get panel using TID or l21.panel_id
            #panel = fetch_or_create_panel(panel_id=row.panel_id, tid=row.tid)
            receive = self.create_or_update_receive( 
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
                #dmis_panel_name = panel.name,
                receive_condition = row.sample_condition,
                )
            #create an aliquot record, will guess specimen type by tid    
            aliquot = self.create_or_update_aliquot( receive=receive , condition=row.sample_condition, primary=True, tid=row.tid, modified=row.modified )
            
        try:
            cursor.close()          
        except:
            pass
            
        return None        
        

    def create_or_update_receive(self, **kwargs ):

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


        receive = Receive.objects.using(lab_db).filter(receive_identifier=receive_identifier)

        if receive:
            receive = Receive.objects.using(lab_db).get(receive_identifier=receive_identifier)
            if receive.modified < modified:
                if self.debug:
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
                if self.debug:
                    print 'no change for receive %s' % receive_identifier                        
        else:
            protocol = self.fetch_or_create_protocol(protocol_identifier)
            account = self.fetch_or_create_account(protocol_identifier)
            site = self.fetch_or_create_site(site_identifier)        
            patient = self.create_or_update_patient(
                                        account = account, 
                                        subject_identifier = subject_identifier, 
                                        gender=gender, 
                                        dob=dob, 
                                        initials=initials,
                                        )
            receive = Receive.objects.using(lab_db).create(
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
            if self.debug:            
                print 'receive created for sample '+receive_identifier+' protocol '+ protocol_identifier


        return receive
        
    def fetch_or_create_site(self,  site_identifier ):

        if site_identifier == None or site_identifier == '' or site_identifier == '-9':
            site_identifier = '00'
            
        site = Site.objects.using(lab_db).filter(site_identifier__iexact=site_identifier)

        if site:
            site = Site.objects.using(lab_db).get(site_identifier__iexact=site_identifier)
        else:
            oLocation = Location.objects.using(lab_db).filter(name__exact='UNKNOWN')
            if oLocation:
                oLocation = Location.objects.using(lab_db).get(name__exact='UNKNOWN')        
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

    def fetch_or_create_protocol(self,  protocol_identifier ):

        protocol = Protocol.objects.using(lab_db).filter(protocol_identifier__iexact=protocol_identifier)
        
        if protocol:
            protocol = Protocol.objects.using(lab_db).get(protocol_identifier__iexact=protocol_identifier)
        else:
            oPI = PrincipalInvestigator.objects.using(lab_db).get(last_name='UNKNOWN')
            oSL = SiteLeader.objects.using(lab_db).get(last_name='UNKNOWN')                
            oFS = FundingSource.objects.using(lab_db).get(name='UNKNOWN')                

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

    def fetch_or_create_account(self,  account_name ):

        account = Account.objects.using(lab_db).filter(account_name__iexact=account_name)
        
        if account:
            account = Account.objects.using(lab_db).get(account_name__iexact=account_name)
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
        
    def create_or_update_patient(self,  **kwargs ):

        subject_identifier = kwargs.get('subject_identifier').strip(' \t\n\r')
        initials = kwargs.get('initials').strip(' \t\n\r')
        if not initials:
            initials = 'X0X'
        account = kwargs.get('account')
        gender = kwargs.get('gender')
        dob = kwargs.get('dob')
        is_dob_estimated = '-'

        patient = Patient.objects.using(lab_db).filter(subject_identifier__iexact=subject_identifier)
        if patient:
            patient = Patient.objects.using(lab_db).get(subject_identifier__iexact=subject_identifier)
            patient.dob = dob
            patient.gender = gender
            patient.is_dob_estimated = is_dob_estimated
            patient.initials = initials
            patient.save()
        else:
            patient = Patient.objects.using(lab_db).create(
                subject_identifier = subject_identifier,
                initials = initials,
                gender = gender,
                dob = dob,
                is_dob_estimated = is_dob_estimated,
                comment = 'auto created / imported from DMIS',            
                )
            patient.account.add(account)        
        return patient    


    def create_or_update_aliquot(self,  **kwargs ):

        receive = kwargs.get('receive')
        condition = kwargs.get('condition')
        tid = kwargs.get('tid')
        modified = kwargs.get('modified')    
        
        aliquot_condition = self.create_or_update_aliquotcondition( condition=condition )

        #create primary
        # TODO: need more detail here for sample types other than the ones listed here...
        create = {}
        if tid == '411':
            create['type'] = '02' #WB
            create['medium'] = 'DBS'
        else:
            create['type'] = '02' #WB
            create['medium'] = 'TUBE'
        
        # get or create the primary aliquot
        aliquot_identifier = '%s0000%s01' % (receive.receive_identifier, create['type'])    
        if Aliquot.objects.using(lab_db).filter(aliquot_identifier__iexact=aliquot_identifier):
            primary_aliquot = Aliquot.objects.using(lab_db).get(aliquot_identifier__iexact=aliquot_identifier)
            if not primary_aliquot.modified == modified:        
                aliquot_type = AliquotType.objects.using(lab_db).get(numeric_code__exact=create['type'])        
                primary_aliquot.modified = modified
                primary_aliquot.aliquot_type = aliquot_type
                primary_aliquot.condition = aliquot_condition
                primary_aliquot.save()
        else:
            create['comment'] = 'auto created on import from DMIS'
            aliquot_type = AliquotType.objects.using(lab_db).get(numeric_code__exact=create['type'])
            aliquot_medium = AliquotMedium.objects.using(lab_db).get(short_name__iexact=create['medium'])            
            primary_aliquot = Aliquot.objects.using(lab_db).create(
                aliquot_identifier = aliquot_identifier,
                receive = receive,
                count = 1,
                aliquot_type = aliquot_type,
                medium = aliquot_medium,
                condition = aliquot_condition,
                comment = create['comment'],            
                )
            #aliquot.account.add(account)        

        

        return primary_aliquot

    def create_or_update_aliquotcondition(self,  **kwargs ):

        if AliquotCondition.objects.using(lab_db).filter(short_name__exact=kwargs.get('condition')):
            aliquot_condition = AliquotCondition.objects.using(lab_db).get(short_name__exact=kwargs.get('condition'))
        else:        
            agg = AliquotCondition.objects.using(lab_db).aggregate(Max('display_index'),)
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

