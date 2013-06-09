# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_household.models import Household
from mochudi_map.helpers import get_sections, prepare_map_points, get_regions, get_icons


def set_section(request):
    """Plot households of a the whole ward to assign a ward section by selecting households.

    Filter points to plot by sending coordinates of a selected ward and section only to the households.html template.
    example of selected criteria; ward: makgophana, section: SECTION A
    **Template:**

    :template:`mochudi_map/templates/household.html`
    """
    template = 'assign_section.html'
    item_region_field = 'ward'
    has_items = False
    households = []
    identifiers = request.session.get('identifiers', [])
    action_script_url = '/mochudi_map/sections/?household_identifiers='

    cart_size = len(identifiers)

    sections = get_sections()

    ward_sections = []
    selected_ward = request.POST.get('ward')
    request.session['icon'] = request.POST.get('marker_icon')

    if Household.objects.filter(ward=selected_ward, ward_section__isnull=True, target=1).exists():
        has_items = True
        households = Household.objects.filter(ward=selected_ward, ward_section__isnull=True, target=1)

    icon = str(request.session['icon'])
    for section in sections:
        ward_sections.append(section)

    payload = prepare_map_points(households,
        icon,
        identifiers,
        'mark'
        )

    if payload:
        has_items = True
    return render_to_response(
        template, {
            'payload': payload,
            'action_script_url': action_script_url,
            'regions': get_regions(),
            'selected_ward': selected_ward,
            'selected_icon': request.session['icon'],
            'icons': get_icons(),
            'sections': get_sections(),
            'option': 'plot',
            'has_items': has_items,
            'item_region_field': item_region_field,
            'show_map': 1,
            'identifiers': identifiers,
            'cart_size': cart_size
            },
            context_instance=RequestContext(request)
        )