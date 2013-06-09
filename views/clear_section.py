# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_mapping.helpers import get_regions, get_icons, get_sections
from bhp_mapping.classes import mapper


def clear_section(request):
    """Assigns selected section to None for all items in a region.

    Filters the households by ward and assigns the ward_section field to Null for the whole ward
    This allows for re-assigning of ward section for households within a ward.
    """
    item_model_cls = mapper.get_item_molde_cls()
    item_label = item_model_cls._meta.object_name
    #item_region_field = 'ward'
    region_label = 'ward'
    item_region_field = 'ward'
    item_section_field = 'ward_section'

    selected_region = request.POST.get('region')
    items = item_model_cls.objects.filter(**{item_region_field: selected_region})
    if items:
        for item in items:
            setattr(item, item_section_field, None)
            item.save()
    cart_size = 0
    identifiers = []
    icon = request.session.get('icon', None)
    if 'identifiers' in request.session:
        cart_size = len(request.session['identifiers'])
        identifiers = request.session['identifiers']
    return render_to_response(
            'map_section.html', {
                'regions': get_regions(),
                'region_label': region_label,
                'item_label': item_label,
                'icons': get_icons(),
                'sections': get_sections(),
                'session_icon': icon,
                'cart_size': cart_size,
                'identifiers': identifiers,
                'show_map': 0,
                'has_items': True,
            },
            context_instance=RequestContext(request)
        )
