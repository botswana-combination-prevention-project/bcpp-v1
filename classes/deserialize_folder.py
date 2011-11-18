import re
import os
from subprocess import call
from django.core.management import setup_environ
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Couldn't find the settings.py module.")
    sys.exit(1)


setup_environ(settings)
from django.core import serializers
from bhp_netbook.models import Netbook
from bhp_serialize.models import SerializedModel


def deserialize_updates( **kwargs):


exit_codes = (
(0, 'Success'),
(1, 'Syntax or usage error'),
(2, 'Protocol incompatibility'),
(3, 'Errors selecting input/output files, dirs'),
(4, 'Requested action not supported: an attempt was made to manipulate 64-bit files on a platform that cannot support them; or an option was specified that is supported by the client and not by the server.'),
(5, 'Error starting client-server protocol'),
(10, 'Error in socket I/O'),
(11, 'Error in file I/O'),
(12, 'Error in rsync protocol data stream'),
(13, 'Errors with program diagnostics'),
(14, 'Error in IPC code'),
(20, 'Received SIGUSR1 or SIGINT'),
(21, 'Some error returned by waitpid()'),
(22, 'Error allocating core memory buffers'),
(23, 'Partial transfer due to error'),
(24, 'Partial transfer due to vanished source files'),
(30, 'Timeout in data send/receive'),
)


# run on community server
# trigger rsync to move files from source top destination
# get information from a model

#netbook_name = kwargs.get('netbook')
#if Netbook.objects.filter(name=kwargs.get('netbook')):

#    netbook = Netbook.objects.get(name=kwargs.get('netbook'))
    
user = 'erikvw'
source_folder = '/home/erikvw/source/bhp041_new2/media/in/'
#destination_folder = '/home/erikvw/source/bhp041_new/media/%s/' % netook.name
destination_folder = '/home/erikvw/source/bhp041_new/media/'
host = '192.168.157.2'

# check destination exists
if not os.path.exists(destination_folder):
    os.mkdir(os.path.expanduser(destination_folder))

# rsync files
cmd = ["rsync", "-avz", "--remove-source-files", "%s@%s:%s*.json" % (user, host, source_folder), destination_folder ]
ret_code = call(cmd)
# check return code
for exit_code in exit_codes:
    if ret_code == exit_code[0]:
        ret_code = exit_code
        break
# if Success, process files
if ret_code[0] == 0:
    # get list of files from destination_folder which is local
file_list = listdir(destination_folder)
# remove files not correct file name format
regex = re.compile(r'[0-9]{20}\-[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')    
for x in range(0,len(file_list)-1):
    if not regex.match(file_list[x]):
        del file_list[x]
#sort as they were named by %Y%m%d%H%M%S%f, see save method for class MyBasicUuidModel 
file_list.sort()

# itearte on the list and ...
for f in file_list:
    fname = '%s/%s' % (settings.MEDIA_ROOT, f,)
    archive_fname = '%s/%s.archive' % (settings.MEDIA_ROOT, f,)          
    fd = open(fname, "r")
    obj = serializers.deserialize("json", stream=fd)
    fd.close()
    obj
    
    rename(fname, archive_fname)      
    obj.save()
    # update log model
    # update activity model

# end and update with success or failure


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--netbook", dest="netbook",
                      help="netbook", metavar="NETBOOK")
    (options, args) = parser.parse_args()


    deserialize_updates(netbook=netbook,)

