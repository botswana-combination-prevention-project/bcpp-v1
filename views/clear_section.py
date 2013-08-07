# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def clear_section(request, **kwargs):
    """Assigns selected section to None for all items in a region.

    Filters the items by ward and assigns the ward_section field to Null for the whole ward
    This allows for re-assigning of ward section for items within a ward.
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)() 
        selected_region = request.POST.get(m.get_region_field_attr())
        items = m.get_item_model_cls().objects.filter(**{m.region_field_attr: selected_region})
        if items:
            for item in items:
                setattr(item, m.region_field_attr, None)
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
                    'mapper_name': mapper_name,
                    'regions': m.get_regions(),
                    'region_label': m.get_region_label(),
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
