import sys,os
sys.path.append('/home/django/source/')
sys.path.append('/home/django/source/bhplab/')
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
from lab_import_dmis.classes import DmisOrder


def fetch_order(**kwargs):
    
    dmis_order = DmisOrder()
    dmis_order.fetch_order(**kwargs)
    
if __name__ == "__main__":
    
    print 'fetching lab orders from dmis....'
    print 'fetching orders....'
    if len(sys.argv) > 1:
        fetch_order(subject_identifier=sys.argv[1], lab_db=sys.argv[2])
    else:
        fetch_order()
    print 'Done'
    sys.exit (0)                  
