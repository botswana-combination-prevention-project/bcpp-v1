from django.conf import settings
from bhp_common.utils import os_variables

defaults = {
    'extend': "base_site.html", #required, but this default will avoid an error           
    'template': 'search.html',
    'report_title': "",
    'section_name': "",
    'os_variables': os_variables,
    'sql':"",
    'database': settings.DATABASES['default'],
    'base_search_extender': "section.html",
    'search_results': "",
    'dbname':"default",
    'page': 0,
    'magic_url': '',
    'search_results': None,
    'search_result_title': 'Results',
    }