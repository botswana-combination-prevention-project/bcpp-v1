from settings import DATABASES
from bhp_common.utils import os_variables

TEMPLATE_CONTEXT = {
    'extend': "base_site.html", #required, but this default will avoid an error           
    'template': "", #required
    'report_title': "",
    'section_name': "",
    'os_variables': os_variables,
    'sql':"",
    'database': DATABASES['default'],
    } 
