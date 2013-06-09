# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_map.choices import ICONS
from mochudi_map.helpers import get_regions, get_sections
from mochudi_household.models import Household


def empty_cart(request, message):
    """Empties cart.    """
    template = 'map_index.html'
    item_model_cls = Household
    #item_region_field = 'ward'
    region_label = 'ward'

    try:
        del request.session['identifiers']
        del request.session['icon']
    except KeyError:
        pass

    return render_to_response(
            template, {
                'regions': get_regions(),
                'sections': get_sections(),
                'icons': ICONS,
                'message': message,
                'item_label': item_model_cls._meta.object_name,
                'region_label': region_label,
            },
            context_instance=RequestContext(request)
        )
