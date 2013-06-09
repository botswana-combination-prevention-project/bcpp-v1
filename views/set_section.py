# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def set_section(request):
    """Plot items of a the whole ward to assign a ward section by selecting items.

    Filter points to plot by sending coordinates of a selected ward and section only to the households.html template.
    example of selected criteria; ward: makgophana, section: SECTION A
    **Template:**

    :template:`mochudi_map/templates/household.html`
    """
    template = 'assign_section.html'
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        #item_region_field = 'ward'
        has_items = False
        items = []
        identifiers = request.session.get('identifiers', [])
        action_script_url = '/bhp_map/sections/?household_identifiers='
        cart_size = len(identifiers)
        sections = m.get_sections()
        ward_sections = []
        selected_ward = request.POST.get('ward')
        request.session['icon'] = request.POST.get('marker_icon')
        if m.item_model_cls.objects.filter(ward=selected_ward, ward_section__isnull=True, target=1).exists():
            has_items = True
            items = m.item_model_cls.objects.filter(ward=selected_ward, ward_section__isnull=True, target=1)

        icon = str(request.session['icon'])
        for section in sections:
            ward_sections.append(section)

        payload = m.prepare_map_points(items,
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
                'regions': m.get_regions(),
                'selected_ward': selected_ward,
                'selected_icon': request.session['icon'],
                'icons': m.get_icons(),
                'sections': m.get_sections(),
                'option': 'plot',
                'has_items': has_items,
                'item_region_field': m.region_field_attr,
                'show_map': 1,
                'identifiers': identifiers,
                'cart_size': cart_size
                },
                context_instance=RequestContext(request)
            )
