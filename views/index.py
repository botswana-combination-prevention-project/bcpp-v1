from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_map.choices import ICONS
from mochudi_map.helpers import get_regions, get_sections


def index(request):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'map_index.html'
    region_label = 'ward'
    cart_size = 0
    identifiers = []
    icon = request.session.get('icon', None)
    if 'identifiers' in request.session:
        cart_size = len(request.session['identifiers'])
        identifiers = request.session['identifiers']
    return render_to_response(
            template, {
                'region_label': region_label,
                'regions': get_regions(),
                'sections': get_sections(),
                'icons': ICONS,
                'session_icon': icon,
                'cart_size': cart_size,
                'identifiers': identifiers
            },
            context_instance=RequestContext(request)
        )
