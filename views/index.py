from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def index(request):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'map_index.html'
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                template, {
                    'region_label': m.region_label,
                    'regions': m.get_regions(),
                    'sections': m.get_sections(),
                    'icons': m.get_icons(),
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers
                },
                context_instance=RequestContext(request)
            )
