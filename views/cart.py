## Import django modules
#from django.shortcuts import render_to_response
#from django.template import RequestContext
##from django.http import HttpResponse
#from django.core.exceptions import ObjectDoesNotExist
#from mochudi_household.models import Household
#from bhp_dispatch.models import Dispatch
#from bhp_sync.models import Producer
#from mochudi_map.choices import ICONS
#from mochudi_map.helpers import get_wards_list, session_to_string, prepare_map_points
#
#
#def add_to_cart(request):
#    """Adds list of identifiers to a shopping cart and return back to map or checkout cart.
#
#    The list of identifiers of points that are within a polygon.
#
#    Uses template :template:`mochudi_map/templates/households.html`
#    """
#    message = ""
#    is_error = False
#    household_identifiers = None
#    identifiers = []
#    payload = []
#    cart_size = 0
#    cart = None
#    ids = request.GET.get('household_identifiers')
#    if ids:
#        household_identifiers = ids.split(",")
#
#    try:
#        if household_identifiers:
#            if 'identifiers' in request.session:
#                # Merge identifiers in the session with the new ones removing duplicates
#                merged = list(set(request.session['identifiers'] + household_identifiers))
#                request.session['identifiers'] = merged
#            else:
#                request.session['identifiers'] = household_identifiers
#
#            identifiers = request.session['identifiers']
#            cart_size = len(request.session['identifiers'])
#            cart = session_to_string(request.session['identifiers']),
#            #message = "Households {0} added to shopping cart!".format(session_to_string(household_identifiers,False))
#        else:
#            message = "No household we selected"
#            is_error = True
#    except:
#        message = "Oops! something went wrong!"
#        is_error = True
#
#    households = Household.objects.filter(household_identifier__in=household_identifiers)
#    icon = request.session['icon']
#    payload = prepare_map_points(households,
#        icon,
#        request.session['identifiers'],
#        'red-circle'
#        )
#
#    return render_to_response(
#            'map.html', {
#                'payload': payload,
#                'identifiers': identifiers,
#                'cart': cart,
#                'cart_size': cart_size,
#                'message': message,
#                'option': 'save',
#                'icons': ICONS,
#                'is_error': is_error,
#                'show_map': 0
#            },
#            context_instance=RequestContext(request)
#        )
#
#
#def checkout_cart(request):
#    """Previews selected households in the dispatch cart.
#
#    At the point the use has following options:
#        1. Select producer to save the cart (possibly start another session).
#        2. Choose to preview the households on the map.
#        3. Continue more households to the cart.
#        4. Removed some of the households from the cart
#
#    Uses template :template:`mochudi_map/templates/view_cart.html`
#    """
#    households = []
#    payload = []
#    identifiers = request.session.get('identifiers', [])
#    cart_size = len(identifiers)
#    icon = request.session.get('icon', None)
#    option = request.GET.get('option', 'save')
#    producers = Producer.objects.all().order_by('name')
#    if option == 'preview':
#        households = Household.objects.filter(household_identifier__in=identifiers)
#        payload = prepare_map_points(households,
#            icon,
#            identifiers,
#            'red-circle'
#            )
#
#    return render_to_response(
#        'view_cart.html', {
#            'payload': payload,
#            'netbooks': producers,
#            'identifiers': identifiers,
#            'cart_size': cart_size,
#            'selected_icon': icon,
#            'option': option
#            },
#            context_instance=RequestContext(request)
#        )
#
#
#def empty_cart(request, message):
#    """Empties cart.
#
#    Uses template :template:`mochudi_map/templates/households_index.html`
#    """
#    try:
#        del request.session['identifiers']
#        del request.session['icon']
#    except KeyError:
#        pass
#
#    producers = Producer.objects.all().order_by('name')
#    return render_to_response(
#            'households_index.html', {
#                'netbooks': producers,
#                'wards': get_wards_list(),
#                'icons': ICONS,
#                'message': message
#            },
#            context_instance=RequestContext(request)
#        )
#
#
#def update_cart(request):
#    """Removes household identifier(s) from cart.
#
#    Uses template :template:`mochudi_map/templates/view_cart.html`
#    """
#    update_error = 0
#    households = []
#    payload = []
#    message = None
#    deleted_ids = request.POST.getlist('identifiers')
#
#    # We have household identifiers to remove from cart
#    if deleted_ids:
#        if len(deleted_ids) == 0:
#            message = "Please select at least one household to remove from the cart"
#            update_error = 1
#        else:
#            if 'identifiers' in request.session:
#                a = request.session['identifiers']
#                request.session['identifiers'] = [x for x in a if x not in deleted_ids]
#                message = "{0} was/were removed".format(session_to_string(deleted_ids, False))
#
#    identifiers = request.session['identifiers']
#    cart_size = len(request.session['identifiers'])
#
#    icon = request.session.get('icon', None)
#    producers = Producer.objects.all().order_by('name')
#    option = request.POST.get('option', 'save')
#    if option == 'preview':
#        households = Household.objects.filter(household_identifier__in=identifiers)
#        icon = request.session['icon']
#        # Get list of points to map from a list of households
#        payload = prepare_map_points(households,
#            icon,
#            request.session['identifiers'],
#            'red-circle'
#            )
#
#    return render_to_response(
#        'view_cart.html', {
#            'payload': payload,
#            'netbooks': producers,
#            'identifiers': identifiers,
#            'cart_size': cart_size,
#            'selected_icon': icon,
#            'message': message,
#            'option': option,
#            'update_error': update_error
#            },
#            context_instance=RequestContext(request)
#        )
#
#
#def save_cart(request):
#    """Saves the dispatch cart to the database as an instance of model Dispatch.
#
#    Uses template :template:`mochudi_map/templates/view_cart.html`
#    """
#
#    #Initialize variables
#    dispatch_items = ""
#    cart_size = 0
#    icon = None
#    is_error = 0
#    message = None
#    option = None
#    households = []
#    payload = []
#    identifiers = []
#    wards = None
#    producer_pk = None
#    template = "households_index.html"
#    # TODO: make this producer, not netbook. Or get to the producer from netbook
#    producer_name = request.POST.get('netbook')
#    producers = Producer.objects.all().order_by('name')
#    try:
#        # Get selected producer from our list of producers
#        producer = Producer.objects.get(name=producer_name)
#        producer_pk = producer.pk
#        #Make sure we have household identifiers in our session
#        if 'identifiers' in request.session:
#            if len(request.session['identifiers']) > 0:
#                # create dispatch_items from the list of household
#                # identifiers by with each identifier on a single line
#                for household_identifier in request.session['identifiers']:
#                    dispatch_items = dispatch_items + "{0} \n".format(household_identifier)
#
#                #create an instance of HBCDispatch to send a list to a selected producer
#                Dispatch.objects.create(
#                    producer=producer,
#                    dispatch_items=dispatch_items
#                    )
#                # Clear cart to start a new session
#                message = "The following households were dispatched: {0}".format(dispatch_items)
#                #empty cart
#                try:
#                    del request.session['identifiers']
#                    del request.session['icon']
#                except KeyError:
#                    pass
#
#            else:
#                # Cart was empty
#                pass
#    except ObjectDoesNotExist:
#        message = "Oops! Selected producer not found not found in database"
#        is_error = 1
#    except:
#        message = "Oops! Something went wrong"
#
#    # An error occurred! We have to show the cart checkout screen again!
#    if is_error == 1:
#        template = 'view_cart.html'
#        if 'identifiers' in request.session:
#            identifiers = request.session['identifiers']
#            cart_size = len(identifiers)
#
#        icon = request.session.get('icon', None)
#        option = request.POST.get('option', 'save')
#        if option == 'preview':
#            households = Household.objects.filter(household_identifier__in=identifiers)
#            icon = request.session['icon']
#            # Get list of points to map from a list of households
#            payload = prepare_map_points(households,
#                icon,
#                request.session['identifiers'],
#                'red-circle'
#                )
#    else:
#        cart_size = 0
#        wards = get_wards_list()
#
#    return render_to_response(
#        template, {
#            'payload': payload,
#            'netbooks': producers,
#            'netbook_pk': producer_pk,
#            'identifiers': identifiers,
#            'wards': wards,
#            'cart_size': cart_size,
#            'selected_icon': icon,
#            'message': message,
#            'option': option,
#            'icons': ICONS,
#            'is_error': is_error
#            },
#            context_instance=RequestContext(request)
#        )
#
#
#def save_map(request):
#    """Create dipatch from the selected households.
#
#    The list of identifiers of points that are within a polygon a sent to a producer that has been selected.
#    Redirect back to the map to do a selection of a ward again.
#
#    Uses :template:`mochudi_map/templates/households_index.html`
#    """
#    msg = ""
#    checkout_items = ""
#    household_identifiers = None
#    identifiers = request.GET.get('household_identifiers')
#    """Get producer name from the template"""
#    producer_name = request.GET.get('netbook')
#
#    if identifiers:
#        household_identifiers = identifiers.split(",")
#
#    try:
#        producer = Producer.objects.get(name=producer_name)
#        if household_identifiers:
#            for household_identifier in household_identifiers:
#                checkout_items = checkout_items + "{0} \n".format(household_identifier)
##            #create an instance of CheckoutHousehold to send a list to a selected producer
#            Dispatch.objects.create(
#                producer=producer,
#                checkout_items=checkout_items
#                )
#            msg = "Households {0} added to 'shopping cart'!".format(identifiers)
#        else:
#            msg = "No household we selected"
#    except:
#        msg = "Oop! something went wrong!"
#
#    households = {}
#    return render_to_response(
#            'households_index.html', {
#                'households': households,
#                'cart': request.session['identifiers'],
#                'cart_size': len(request.session['identifiers']),
#                'ward': request.session['ward'],
#                'message': msg,
#                'option': 'save',
#                'icons': ICONS
#            },
#            context_instance=RequestContext(request))