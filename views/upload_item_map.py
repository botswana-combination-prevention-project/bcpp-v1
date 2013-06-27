from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def handle_uploaded_file(f, identifier):
    """Copies uploaded map image file to settings.MAP_DIR."""
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
def upload_item_map(request, **kwargs):
    """Uploads item map saved on disk as an images e.g google map screenshot."""
    identifier = request.POST.get('identifier')
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        m = mapper.get_registry(mapper_name)()
        filename = handle_uploaded_file(request.FILES['file'], identifier)
        if filename:
            item = m.get_item_model_cls().objects.get(Q(**{'{0}__in'.format(m.get_identifier_field_attr()): identifier}))
            item.uploaded_map = filename
            item.save()
        return HttpResponseRedirect('{% url "section" mapper_name %}')
