# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_mapping.choices import ICONS
from bhp_mapping.helpers import session_to_string, prepare_map_points
from bhp_mapping.classes import mapper


def add_to_cart(request):
    """Adds a list of identifiers to a shopping cart and returns back to map or checkout cart.

    The list of identifiers of points that are within a polygon.

    Uses template :template:`mochudi_map/templates/households.html`
    """
    template = 'map.html'
    item_model_cls = mapper.get_item_model_cls()
    item_label = item_model_cls._meta.object_name
    item_identifier_field = 'household_identifier'
    additional_item_identifiers = request.GET.get('household_identifiers')  # TODO: change the template variable name
                                                                            #        Could this be item_identifier_field?
    message = ""
    is_error = False
    item_identifiers = []
    cart_size = 0
    cart = None
    if additional_item_identifiers:
        additional_item_identifiers = additional_item_identifiers.split(",")

    try:
        if additional_item_identifiers:
            if 'identifiers' in request.session:
                # Merge identifiers in the session with the additional ones, removing duplicates
                request.session['identifiers'] = list(set(request.session['identifiers'] + additional_item_identifiers))
            else:
                request.session['identifiers'] = additional_item_identifiers

            item_identifiers = request.session['identifiers']
            cart_size = len(request.session['identifiers'])
            cart = session_to_string(request.session['identifiers']),
        else:
            message = "No items were selected"
            is_error = True
    except:
        message = "Oops! something went wrong!"
        is_error = True

    item_instances = item_model_cls.objects.filter(**{'{0}__in'.format(item_identifier_field): item_identifiers})
    icon = request.session['icon']
    payload = prepare_map_points(item_instances,
        icon,
        request.session['identifiers'],
        'mark'
        )

    return render_to_response(
            template, {
                'payload': payload,
                'identifiers': item_identifiers,
                'cart': cart,
                'cart_size': cart_size,
                'message': message,
                'option': 'save',
                'icons': ICONS,
                'is_error': is_error,
                'show_map': 0,
                'item_label': item_label
            },
            context_instance=RequestContext(request)
        )
