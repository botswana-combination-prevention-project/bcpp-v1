# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_map.helpers import get_regions, get_icons
#from mochudi_household.models import Household


def map_section(request):
    """Select ward and section to separate households into section in a ward

    The selected ward and section are going to be use to set a section for the ward selected.

   """
    template = 'map_section.html'
#    item_model_cls = Household
    item_region_field = 'ward'
    region_label = 'ward'

    cart_size = 0
    identifiers = []
    icon = request.session.get('icon', None)
    if 'identifiers' in request.session:
        cart_size = len(request.session['identifiers'])
        identifiers = request.session['identifiers']
    
    return render_to_response(
            template, {
                'regions': get_regions(),
                'icons': get_icons(),
                'item_region_field': item_region_field,
                'region_label': region_label,
                'session_icon': icon,
                'cart_size': cart_size,
                'identifiers': identifiers,
                'show_map': 1,
                'has_items': True,
                'option': 'plot'
            },
            context_instance=RequestContext(request))
