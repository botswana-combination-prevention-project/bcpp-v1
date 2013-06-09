# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_mapping.helpers import prepare_map_points
from mochudi_household.models import Household


def checkout_cart(request):
    """Previews selected households in the cart.

    At the point the use has following options:
        1. Choose to preview the households on the map.
        2. Continue more households to the cart.
        3. Removed some of the households from the cart

    Uses template :template:`mochudi_map/templates/view_cart.html`
    """
    item_model_cls = Household
    item_identifier_field = 'household_identifier'
    template = 'view_cart.html'

    payload = []
    item_identifiers = request.session.get('identifiers', [])
    cart_size = len(item_identifiers)
    icon = request.session.get('icon', None)
    option = request.GET.get('option', 'save')
    if option == 'preview':
        item_instances = item_model_cls.objects.filter(**{'{0}__in'.format(item_identifier_field): item_identifiers})
        payload = prepare_map_points(item_instances,
            icon,
            item_identifiers,
            'mark'
            )

    return render_to_response(
        template, {
            'payload': payload,
            'identifiers': item_identifiers,
            'cart_size': cart_size,
            'selected_icon': icon,
            'option': option
            },
            context_instance=RequestContext(request)
        )
