import os
# Import django modules
#from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
#from django.template import RequestContext
from mochudi_household.models import Household


def handle_uploaded_file(f, identifier):
    """Copies uploaded map image file to settings.MAP_DIR
    """

    filename = None
    if file:
        file_extension = f.content_type.split("/")[1]
        filename = "{0}.{1}".format(identifier, file_extension)
        abs_filename = "{0}{1}".format(settings.MAP_DIR, filename)
        with open(abs_filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    return filename


@login_required
@csrf_protect
def upload_item_map(request):
    """Uploads item map saved on disk as an images e.g google map screenshot.
    """
    identifier = request.POST.get('identifier')
    

    try:
        filename = handle_uploaded_file(request.FILES['file'], identifier)
        if filename:
            household = Household.objects.get(household_identifier=identifier)
            household.uploaded_map = filename
            household.save()
    except:
        raise

    return HttpResponseRedirect('{% url section %}')
