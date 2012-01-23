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


class DmisOrder(object):

    def __init__(self, debug=False):
        self.debug = debug


    def fetch(self, **kwargs):
        
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
        lab_db = kwargs.get('lab_db', 'default')

        cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
        cursor = cnxn.cursor()

        now  = datetime.today()
        import_datetime = now
        import_tdelta = 7
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
        
        subject_identifier = kwargs.get('subject_identifier')
        if subject_identifier:
            receives = Receive.objects.using(lab_db).filter(patient__subject_identifier__icontains=subject_identifier)
            receive_count = receives.count()
        else:
            receives = Receive.objects.using(lab_db).filter(modified__gte=last_import_datetime).order_by('-modified')
            receive_count = receives.count()

        tot=receive_count
        for receive in receives:
            print '%s %s/%s' % (receive.receive_identifier, receive_count, tot)
            receive_count -= 1
            sql = 'select l21.id as order_identifier, l21.headerdate as order_datetime, l21.keyopcreated as user_created,\
                    l21.keyoplastmodified as user_modified, l21.datecreated as created, l21.datelastmodified as modified,\
                    convert(varchar(50), l21.result_guid) as result_guid, \
                    l21.id as dmis_reference, \
                    l21.panel_id as panel_id \
                    from lab21response as l21 \
                    where l21.pid=\'%s\'' % (receive.receive_identifier)
            
            cursor.execute(str(sql))
            
            for row in cursor:
                panel = self.fetch_or_create_panel(panel_id=row.panel_id, receive_identifier = receive.receive_identifier)
                aliquot = self.fetch_or_create_aliquot(receive=receive, panel=panel)
                # result_guid = row.result_guid.strip(' \t\n\r')
                order = self.create_or_update_order( 
                    order_identifier = row.order_identifier,
                    order_datetime = row.order_datetime,
                    aliquot = aliquot,
                    panel = panel,
                    user_created = row.user_created,
                    user_modified = row.user_modified,
                    created = row.created,
                    modified = row.modified,
                    dmis_reference=row.dmis_reference,
                    )
        try:
            cursor.close()          
        except:
            pass
            
        return None        
        
    def create_or_update_order(self, **kwargs ):

        order_identifier = kwargs.get('order_identifier')
        panel = kwargs.get('panel')
        aliquot = kwargs.get('aliquot')    
        order_datetime = kwargs.get('order_datetime')
        comment = '',
        created = kwargs.get('created')
        modified = kwargs.get('modified')
        user_created = kwargs.get('user_created')
        user_modified = kwargs.get('user_modified')
        dmis_reference = kwargs.get('dmis_reference')                    
     
        orders = Order.objects.using(lab_db).filter(order_identifier = order_identifier )
                
        if orders:
            order = Order.objects.using(lab_db).get(order_identifier = order_identifier )    
        else:
            order = Order.objects.using(lab_db).create(
                order_identifier = order_identifier,
                order_datetime = order_datetime,
                aliquot = aliquot,
                panel = panel,
                comment = '',
                created = created,
                modified = modified,
                user_created = user_created,
                user_modified = user_modified,
                dmis_reference = dmis_reference,
                ) 
            print 'created order'
        return order

    def fetch_or_create_panel(self,**kwargs):

        panel_id = kwargs.get('panel_id')
        receive_identifier = kwargs.get('receive_identifier')
        panel = None
        panel_group_name = None
        # use either panel_id or panel_group_name to either get or create a panel
        # if you have receive_identifier, this may help
        if panel_id and not panel_id == '-9':
            # try to get using row.panel_id
            panels = Panel.objects.using(lab_db).filter(dmis_panel_identifier=panel_id)
            if panels:
                panel = panels[0]
        if not panel and receive_identifier:
            # go back to the receving record and get the TID of the first record, usually only one record returned, but not always...
            cnxn1 = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
            cursor_panel = cnxn1.cursor()
            sql = 'select top 1 tid as panel_group_name from lab01response where pid=\'%s\' order by datecreated'  % (receive_identifier,)
            cursor_panel.execute(str(sql))
            for row in cursor_panel:
                panel_group_name = row.panel_group_name
                panels = Panel.objects.using(lab_db).filter(panel_group__name__exact=panel_group_name)
                if panels:
                    panel = panels[0]

        if not panel:
            #raise TypeError(panel_id)
            # hmmm. still nothing, so just create a dummy panel and move on
            panel_groups = PanelGroup.objects.using(lab_db).filter(name=panel_id)
            if not panel_groups:
                panel_group = PanelGroup.objects.using(lab_db).create(name=panel_id,)
            else:
                panel_group = PanelGroup.objects.using(lab_db).get(name=panel_id,)    
            # create a new panel
            panel = Panel.objects.using(lab_db).create(
                                    name = panel_id,
                                    panel_group = panel_group,
                                    comment = 'temp',
                                    dmis_panel_identifier = panel_id,
                                    )
            print '....created panel for %s ' % (panel_id,)
        return panel

    def fetch_or_create_aliquot(self, **kwargs ):

        receive = kwargs.get('receive')
        panel = kwargs.get('panel')
        tid = panel.panel_group.name
        
        primary_aliquot_identifier_stub = '%s0000' % (receive.receive_identifier)    
        primary_aliquot = Aliquot.objects.using(lab_db).get(aliquot_identifier__icontains=primary_aliquot_identifier_stub)

        #if order is not placed against primary, create child
        # TODO: need more detail here for sample types other than the ones listed here...    
        create = {}
        if tid[0]=='1': #CD4
            create = {}
        elif tid[0]=='2':  
            create['type'] = '06' #WB
            create['medium'] = 'TUBE'
            create['condition'] = '10'                
        elif tid[0]=='3': # CHEM, HAEM    
            create = {}
        elif tid[0]=='4': #VL, RNA   
            create['type'] = '32' #WB
            create['medium'] = 'TUBE'
            create['condition'] = '10'        
        else:
            create = {}        

        if not create:
            aliquot = primary_aliquot
        else:    
            aliquot_identifier = '%s0201%s02' % (receive.receive_identifier, create['type'])    
            create['comment'] = 'auto created on import from DMIS'
            aliquot = Aliquot.objects.using(lab_db).filter(aliquot_identifier__iexact=aliquot_identifier)
            if aliquot:
                aliquot = Aliquot.objects.using(lab_db).get(aliquot_identifier__iexact=aliquot_identifier)
            else:
                aliquot_type = AliquotType.objects.using(lab_db).get(numeric_code__exact=create['type'])
                aliquot_medium = AliquotMedium.objects.using(lab_db).get(short_name__iexact=create['medium'])   
                aliquot_condition = AliquotCondition.objects.using(lab_db).get(short_name__iexact=create['condition'])            
                aliquot = Aliquot.objects.using(lab_db).create(
                    aliquot_identifier = aliquot_identifier,
                    receive = receive,
                    count = 2,
                    aliquot_type = aliquot_type,
                    parent_identifier = primary_aliquot,
                    medium = aliquot_medium,
                    condition=primary_aliquot.condition,
                    comment = create['comment'],            
                    )
                print '....created aliquot from %s ' % (primary_aliquot.aliquot_identifier,)                

        return aliquot

    def create_or_update_aliquotcondition(self, **kwargs ):

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

