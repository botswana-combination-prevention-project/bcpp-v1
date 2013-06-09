from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def empty_cart(request, message):
    """Empties cart.    """
    template = 'map_index.html'
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        try:
            del request.session['identifiers']
            del request.session['icon']
        except KeyError:
            pass
        return render_to_response(
                template, {
                    'regions': m.get_regions(),
                    'sections': m.get_sections(),
                    'icons': m.get_icons(),
                    'message': message,
                    'item_label': m.get_item_model_cls()._meta.object_name,
                    'region_label': m.region_label,
                },
                context_instance=RequestContext(request)
            )
