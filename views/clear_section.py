# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def clear_section(request):
    """Assigns selected section to None for all items in a region.

    Filters the households by ward and assigns the ward_section field to Null for the whole ward
    This allows for re-assigning of ward section for households within a ward.
    """
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        selected_region = request.POST.get('region')
        items = m.get_item_model_cls().objects.filter(**{m.region_field_attr: selected_region})
        if items:
            for item in items:
                setattr(item, m.section_field_attr, None)
                item.save()
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                'map_section.html', {
                    'regions': m.get_regions(),
                    'region_label': m.region_label,
                    'item_label': m.get_item_model_cls._meta.object_name,
                    'icons': m.get_icons(),
                    'sections': m.get_sections(),
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers,
                    'show_map': 0,
                    'has_items': True,
                },
                context_instance=RequestContext(request)
            )
