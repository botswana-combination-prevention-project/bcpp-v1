import os
import platform

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from edc.device.sync.views import export_outgoing_to_file
from edc.map.classes import site_mappers


@login_required
@csrf_protect
def export_outgoing_to_usb(request, **kwargs):
    """Sets the path and then calls the edc export view 'export_outgoing_to_file'."""
    site_name = site_mappers.get_mapper(site_mappers.current_community).map_area
    app_name = settings.APP_NAME.lower()
    if platform.system() == 'Darwin':
        usb_path = '/Volumes/{}_usb/'.format(app_name)
    else:
        usb_path = '/media/{}_usb/'.format(app_name)
    filename = '{}_{}_{}.json'.format(app_name, site_name, str(datetime.now().strftime("%Y%m%d%H%M")))
    path = os.path.join(usb_path, filename)
    return export_outgoing_to_file(request, path, target_name='USB Drive')
