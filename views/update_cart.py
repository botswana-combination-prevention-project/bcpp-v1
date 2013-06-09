# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_household.models import Household
from mochudi_map.helpers import session_to_string, prepare_map_points


def update_cart(request):
    """Removes household identifier(s) from cart.

    Uses template :template:`mochudi_map/templates/view_cart.html`
    """
    update_error = 0
    households = []
    payload = []
    message = None
    deleted_ids = request.POST.getlist('identifiers')

    # We have household identifiers to remove from cart
    if deleted_ids:
        if len(deleted_ids) == 0:
            message = "Please select at least one household to remove from the cart"
            update_error = 1
        else:
            if 'identifiers' in request.session:
                a = request.session['identifiers']
                request.session['identifiers'] = [x for x in a if x not in deleted_ids]
                message = "{0} was/were removed".format(session_to_string(deleted_ids, False))

    identifiers = request.session['identifiers']
    cart_size = len(request.session['identifiers'])

    icon = request.session.get('icon', None)
    option = request.POST.get('option', 'save')
    if option == 'preview':
        households = Household.objects.filter(household_identifier__in=identifiers)
        icon = request.session['icon']
        # Get list of points to map from a list of households
        payload = prepare_map_points(households,
            icon,
            request.session['identifiers'],
            'mark'
            )

    return render_to_response(
        'view_cart.html', {
            'payload': payload,
            'identifiers': identifiers,
            'cart_size': cart_size,
            'selected_icon': icon,
            'message': message,
            'option': option,
            'update_error': update_error
            },
            context_instance=RequestContext(request)
        )