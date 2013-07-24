from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import Mapper, site_mappers
from bhp_map.exceptions import MapperError


def map_index(request, **kwargs):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'map_index.html'
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
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'item_label': m.get_item_label(),
                    'region_field_attr': m.get_region_field_attr(),
                    'region_label': m.get_region_label(),
                    'section_field_attr': m.get_section_field_attr(),
                    'section_label': m.get_section_label(),
                    'regions': m.get_regions(),
                    'sections': m.get_sections(),
                    'icons': m.get_icons(),
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers
                },
                context_instance=RequestContext(request)
            )
    return render_to_response(
            template, {
                'mapper_names': mapper_names,
            },
            context_instance=RequestContext(request)
        )
