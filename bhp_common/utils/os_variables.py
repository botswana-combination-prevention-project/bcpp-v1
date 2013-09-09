import re, socket, sys
import syslog
#from ifconfig import ifconfig
from django import forms
from django.core.exceptions import ValidationError
from bhp_variables.models import StudySpecific

def os_variables():
       
    syslog.syslog('os_variables:')
        
    variables = {}

   
    variables['hostname'] = socket.gethostname()
    variables['wlan_network'] = ""
    variables['warnings'] = []
    
    """

    #netbook checks
    if StudySpecific.objects.all():
        sp = StudySpecific.objects.all()[0]    

        if sp.machine_type == 'NETBOOK':
            try:
                variables['device_id'] = sp.device_id
                if not sp.hostname_prefix:
                    msg = 'StudySpecific.hostname_prefix not set'
                    variables['warnings'].append(msg)        
                    syslog.syslog(syslog.LOG_WARNING, msg)          
            except:
                variables['warnings'].append('StudySpecific variables not set')                
            
            config = {} #ifconfig('wlan0')
            
            if not config['addr'] == '0.0.0.0':
                variables['wlan_ipaddr'] = config['addr'] 
                msg = 'interface wlan0 ipaddr is %s' % (variables['wlan_ipaddr'])
                variables['wlan_network'] = '%s.%s.%s.0/24' % (variables['wlan_ipaddr'].split('.')[0], variables['wlan_ipaddr'].split('.')[1], variables['wlan_ipaddr'].split('.')[2])
                syslog.syslog(syslog.LOG_INFO, msg)
            else:
                msg = 'interface wlan0 is not configured or does not exist! Is wireless card on? (udev/rules.d?)'
                variables['warnings'].append(msg)
                syslog.syslog(syslog.LOG_WARNING, msg)

            try:
                variables['wlan_ipaddr']
            except:        
                variables['wlan_ipaddr'] = ''
                    
            try:
                derived_hostname = '%s%s' % (sp.hostname_prefix, variables['wlan_ipaddr'].split('.')[3].zfill(2))
                if not derived_hostname == variables['hostname'] :
                    msg = 'hostname is %s but should be %s based on ip=%s and hostname_prefix=%s. Check wlan0 config and/or StudySpecific.hostname_prefix' % (variables['hostname'], derived_hostname, variables['wlan_ipaddr'], sp.hostname_prefix)
                    variables['warnings'].append(msg)
                    syslog.syslog(syslog.LOG_ERR, msg)
            except:
                variables['warnings'].append('Cannot check hostname against derived hostname, (StudySpecific variable hostname_prefix, StudySpecific variable device_id and wlan0 ip).')                
        """
    return variables
