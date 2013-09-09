# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
#from bhp_mapping.helpers import prepare_map_points
#from mochudi_household.models import Household
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def checkout_cart(request, **kwargs):
    """Previews selected items in the cart.

    At the point the use has following options:
        1. Choose to preview the items on the map.
        2. Continue more items to the cart.
        3. Removed some of the items from the cart

    Uses template :template:`bhp_map/templates/view_cart.html`
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        template = 'view_cart.html'
        payload = []
        item_identifiers = request.session.get('identifiers', [])
        cart_size = len(item_identifiers)
        icon = request.session.get('icon', None)
        option = request.GET.get('option', 'save')
        landmark_list = []
        landmarks = m.get_landmarks()
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        if option == 'preview':
            item_instances = m.get_item_model_cls().objects.filter(**{'{0}__in'.format(m.identifier_field_attr): item_identifiers})
            payload = m.prepare_map_points(item_instances,
                icon,
                item_identifiers,
                'egg-circle'
                )
        return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'payload': payload,
                'identifiers': item_identifiers,
                'landmarks': landmark_list,
                'cart_size': cart_size,
                'selected_icon': icon,
                'gps_center_lat': m.get_gps_center_lat(),
                'gps_center_lon': m.get_gps_center_lon(),
                'option': option
                },
                context_instance=RequestContext(request)
            )
