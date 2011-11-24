from datetime import date, datetime
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from bhp_nmap.utils import all_uphosts

@dajaxice_register
def list_netbooks(request):

    dajax = Dajax()
    
    uphosts = all_uphosts(network='10.42.43.0/24')    

    rendered = render_to_string('uphosts_include.html', {'uphosts': uphosts })    

    dajax.assign('#netbook_list','innerHTML',rendered)

    return dajax.json()

