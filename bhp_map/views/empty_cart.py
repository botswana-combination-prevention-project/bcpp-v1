from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def empty_cart(request, message, **kwargs):
    """Empties cart.    """
    template = 'map_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        try:
            del request.session['identifiers']
            del request.session['icon']
        except KeyError:
            pass
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'regions': m.get_regions(),
                    'sections': m.get_sections(),
                    'icons': m.get_icons(),
                    'message': message,
                    'item_label': m.get_item_model_cls()._meta.object_name,
                    'region_label': m.get_region_label(),
                },
                context_instance=RequestContext(request)
            )