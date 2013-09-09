# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def set_sub_section(request, **kwargs):
    """Plot items of a the whole ward to assign a ward section by selecting items.

    Filter points to plot by sending coordinates of a selected ward and section only.
    example of selected criteria; ward: makgophana, section: SECTION A
    **Template:**

    :template:`bhp_map/templates/assign_sub_section.html`
    """
    template = 'assign_sub_section.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        #item_region_field = 'ward'
        has_items = False
        items = []
        identifiers = request.session.get('identifiers', [])
        action_script_url = 'save_sub_section_url'
        cart_size = len(identifiers)
        selected_sub_section = request.POST.get(m.get_section_field_attr())
        selected_region = request.POST.get(m.get_region_field_attr())
        request.session['icon'] = request.POST.get('marker_icon')
        if m.item_model_cls.objects.filter(sub_section__isnull=True, section=selected_region).exists():
            has_items = True
            items = m.item_model_cls.objects.filter(sub_section__isnull=True, section=selected_region)

        icon = str(request.session['icon'])
        payload = m.prepare_map_points(items,
            icon,
            identifiers,
            'egg-circle'
            )

        if payload:
            has_items = True
        return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'payload': payload,
                'action_script_url': action_script_url,
                'regions': m.get_regions(),
                'selected_sub_section': selected_sub_section,
                'selected_region': selected_region,
                'selected_icon': request.session['icon'],
                'icons': m.get_icons(),
                'sections': m.get_sections(),
                'gps_center_lat': m.get_gps_center_lat(),
                'gps_center_lon': m.get_gps_center_lon(),
                'option': 'plot',
                'has_items': has_items,
                'item_region_field': m.get_region_field_attr(),
                'item_section_field': m.get_section_field_attr(),
                'show_map': 1,
                'identifiers': identifiers,
                'cart_size': cart_size
                },
                context_instance=RequestContext(request)
            )
