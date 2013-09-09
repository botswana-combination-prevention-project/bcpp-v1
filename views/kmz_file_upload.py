from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import Mapper, site_mappers
from bhp_map.exceptions import MapperError


def kmz_file_upload(request, **kwargs):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'kmz_file_upload.html'
    mapper_name = kwargs.get('mapper_name', '')
    mapper_names = []
    m = None
    if not mapper_name:
        mapper_names = [mname for mname in site_mappers.get_registry()]
    else:
        m = site_mappers.get_registry(mapper_name)
    if m:
        if not issubclass(m, Mapper):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        m = site_mappers.get_registry(mapper_name)()
        
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                },
                context_instance=RequestContext(request)
            )
