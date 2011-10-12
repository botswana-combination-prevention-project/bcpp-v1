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


def fetch_order(**kwargs):
    
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
    last_import_datetime = now - timedelta(days=90)
    import_datetime = now

    #note that some records will not be imported for having>1
    sql  = 'select min(l.id) as dmis_reference, \
            l21.keyopcreated as user_created, \
            l21.keyoplastmodified as user_modified, \
            min(l21.datecreated) as created, \
            min(l21.datelastmodified) as modified, \
            l21.id as order_identifier, \
            l21.panel_id \
            from lab01response as l \
            left join lab21response as l21 on l.pid=l21.pid \
            where l21.id is not null \
            and l.datelastmodified >= \'%s\' \
            and l.datelastmodified <= \'%s\' \
            and sample_date_drawn <= \'%s\' \
            group by l21.keyoplastmodified, l21.id, l21.panel_id  \
            having count(*)=1 \
            order by min(l.id) desc' % (last_import_datetime.strftime('%Y-%m-%d %H:%M'), import_datetime.strftime('%Y-%m-%d %H:%M'), now.strftime('%Y-%m-%d %H:%M'))

    #raise TypeError(sql)

    cursor.execute(sql)

    receives = Receive.objects.filter(modified__gte=last_import_datetime)     
    
    for receive in receives:
        panel = Panel.objects.get(name=receive.dmis_panel_name)
        sql  = 'select l21.id as order_identifier, \
                l21.headerdate as order_datetime,\
                l21.keyopcreated as user_created, \
                l21.keyoplastmodified as user_modified, \
                l21.datecreated) as created, \
                l21.datelastmodified) as modified, \
                l21.panel_id, \
                from lab21response as l21 \
                left join (select pid from lab01response where pid=\'%s\' group by pid) as l on l.pid=l21.pid \
                where l.pid is not null \
                order by l21.id desc' % (receive.receive_identifier,)
        cursor.execute(sql)
     
        for row in cursor:
            panel = fetch_or_create_panel(panel_id=row.panel_id)
            order = create_or_update_order( 
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
    
def create_or_update_order( **kwargs ):

    order_identifier = kwargs.get('order_identifier')
    panel = kwargs.get('panel')
    aliquot = kwargs.get('aliquot')    
    order_datetime = kwargs.get('order_datetime')
    comment = '',
    created = kwargs.get('created')
    modified = kwargs.get('modified')
    dmis_reference = kwargs.get('dmis_reference')                    
 
    orders = Order.objects.filter(order_identifier = order_identifier )
            
    if orders:
        order = Order.objects.get(order_identifier = order_identifier )    
    else:
        order = Order.objects.create(
            order_identifier = order_identifier,
            order_datetime = order_datetime,
            aliquot = aliquot,
            panel = panel,
            comment = '',
            created = created,
            modified = modified,
            dmis_reference = dmis_reference,
            ) 

    return order

def fetch_or_create_panel(**kwargs):
    panel_id = kwargs.get('panel_id')
    panel = None
    if row.panel_id and not panel_id == '-9':
        # try to get using row.panel_id
        panels = Panel.objects.filter(dmis_panel_identifier__exact=panel_id)
        if panels:
            panel = panels[0]
    if not panel:    
        # try using row.tid
        panels = Panel.objects.filter(panel_group__name__exact=tid)
        if panels:
            panel = panels[0]
    if not panel:
        # fetch or create a panel group
        panel_groups = PanelGroup.objects.filter(name=panel_id)
        if not panel_groups:
            panel_group = PanelGroup.objects.create(name=panel_id,)
        else:
            panel_group = PanelGroup.objects.get(name=panel_id,)    
        # create a new panel
        panel = Panel.objects.create(
                                name = panel_id,
                                panel_group = panel_group,
                                comment = 'temp',
                                dmis_panel_identifier = panel_id,
                                )
    return panel

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
    
    print 'fetching lab orders from dmis....'
    print 'fetching orders....'
    fetch_order()
    print 'Done'
    sys.exit (0)                  
