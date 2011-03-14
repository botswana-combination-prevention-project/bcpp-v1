import sys
import nmap
from bhp_common.utils import os_variables
# http://xael.org/norman/python/python-nmap/#usage

def all_uphosts(**kwargs):

    """return a list of up hosts/port in the specified network"""
    
    variables = os_variables()
    hosts = variables['wlan_network']
    if not hosts:
        hosts='192.168.1.0/24'

    # a port scan requires root access ( ... -PE -PA80 )
    #port = kwargs.get('port')
    #if not port:
    #    port=80

    hostname_prefix = kwargs.get('hostname_prefix')
    if not hostname_prefix:
        hostname_prefix='mpp'

    app_name = kwargs.get('app_name')
    if not app_name:
        app_name = 'myapp'


    nm = nmap.PortScanner()
    nm.scan( hosts=hosts, arguments='-n -sP' )
    
    uphosts = {}
    hosts_list = [(x, nm[x.__str__()]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        if status == 'up':
            hostname = '%s%s' % (hostname_prefix, host.split('.')[3].zfill(2))
            url = 'http://%s/%s' % ( host, app_name )
            uphosts[hostname] = { 'host': host, 'hostname':hostname, 'url': url }

    return uphosts
