# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def plot_item_points(request):
    """Plot households from base selection criteria.

      * Filter points to plot by sending coordinates of a selected ward only to the households.html template.
      * Regions contain sections    """
    # TODO: difference in ward ward section selected section and section ??? very confusing
            # docstring Comment is out of date?
    template = 'map.html'
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        item_target_field = 'target'
        # TODO:
        action_script_url = '/mochudi_map/add_cart/?household_identifiers='
        has_items = False
        item_label = m.get_item_model_cls._meta.object_name
        identifiers = request.session.get('identifiers', [])
        selected_section = request.POST.get('section')
        cart_size = len(identifiers)
        cso_icon_dict = []
        section_color_code_list = []
        selected_region = request.POST.get(m.region_field_attr)  # TODO: this should not be "ward" on the template
        request.session['icon'] = request.POST.get('marker_icon')
        if selected_section == 'All':
            items = m.get_item_model_cls.objects.filter(
                Q(**{m.region_field_attr: selected_region, item_target_field: 1}) |
                Q(**{'{0}__in'.format(m.identifier_field_attr): identifiers}))
        else:
            items = m.get_item_model_cls.objects.filter(
                Q(**{m.region_field_attr: selected_region, m.section_field_attr: selected_section, item_target_field: 1}) |
                Q(**{'{0}__in'.format(m.identifier_field_attr): identifiers, m.section_field_attr: selected_section, item_target_field: 1}))
        icon = str(request.session['icon'])
        print selected_section
        payload = m.prepare_map_points(items,
            icon,
            identifiers,
            'mark',
            'red-circle', selected_section)
        if selected_section != "ALL":
            for lon, lat, identifier_label, icon, other_identifier_label in payload:
                icon_name_length = len(icon)
                icon_label = icon[icon_name_length - 1]
                #print icon_label
                cso_icon_dict.append([icon_label, other_identifier_label])
        if selected_section == "All":
            section_color_codes = m.make_dictionary(m.get_other_icons(), m.get_sections())
        else:
            section_color_codes = m.make_dictionary(m.get_icons(), m.get_sections())
        for key_color, sec_value in section_color_codes.iteritems():
            section_color_code_list.append([key_color[:-1], sec_value])
        if payload:
            has_items = True
        return render_to_response(
            template, {
                'payload': payload,
                'action_script_url': action_script_url,
                'has_items': has_items,
                'item_label': item_label,
                'selected_region': selected_region,
                'selected_icon': request.session['icon'],
                'icons': m.get_icons(),
                'option': 'plot',
                'show_map': 1,
                'identifiers': identifiers,
                'cart_size': cart_size,
                'cso_icon_dict': cso_icon_dict,
                'section_color_code_list': section_color_code_list,
                'selected_section': selected_section
                },
                context_instance=RequestContext(request)
            )
