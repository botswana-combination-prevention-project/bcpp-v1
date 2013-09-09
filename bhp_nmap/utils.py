import sys
import nmap
from bhp_common.utils import os_variables
# http://xael.org/norman/python/python-nmap/#usage

def all_uphosts(**kwargs):

    """return a list of up hosts/port in the specified network"""
    
    network = kwargs.get('network', None)
    if not network:
        variables = os_variables()
        network = variables['wlan_network']
    if not network or network == '0.0.0.0/24':
        network='192.168.11.0/24'

    hostname_prefix = kwargs.get('hostname_prefix')
    if not hostname_prefix:
        hostname_prefix='mpp'

    app_name = kwargs.get('app_name')
    if not app_name:
        app_name = ''
   
    nm = nmap.PortScanner()
    nm.scan( hosts=network, arguments='-n -sP' )
    
    uphosts = {}

    hosts_list = [(x, nm[x.__str__()]['status']['state']) for x in nm.all_hosts()]
   
    for host, status in hosts_list:
        if status == 'up':
            hostname = '%s%s' % (hostname_prefix, host.split('.')[3].zfill(2))
            url = 'http://%s/%s' % ( host, app_name )
            uphosts[hostname] = { 'host': host, 'hostname':hostname, 'url': url }

    return uphosts
