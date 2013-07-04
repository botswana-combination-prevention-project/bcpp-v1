# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from bhp_map.classes import site_mapper
from bhp_map.exceptions import MapperError


def plot_item_points(request, **kwargs):
    """Plot items from base selection criteria.

      * Filter points to plot by sending coordinates of a selected ward only to the items.html template.
      * Regions contain sections    """
    # TODO: difference in ward ward section selected section and section ??? very confusing
            # docstring Comment is out of date?
    template = 'map.html'
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')

    if not site_mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        m = site_mapper.get_registry(mapper_name)()
        item_target_field = 'target'
        action_script_url_name = 'map_add_cart_url'
        has_items = False
        mapper_mapper_item_label = m.get_item_label()
        identifiers = request.session.get('identifiers', [])
        selected_section = request.POST.get(m.get_section_field_attr())
        cart_size = len(identifiers)
        cso_icon_dict = []
        section_color_code_list = []
        selected_region = request.POST.get(m.get_region_field_attr())
        request.session['icon'] = request.POST.get('marker_icon')
        if selected_section == 'All':
            items = m.get_item_model_cls().objects.filter(
                Q(**{m.get_region_field_attr(): selected_region, item_target_field: 1}) |
                Q(**{'{0}__in'.format(m.get_identifier_field_attr()): identifiers}))
        else:
            items = m.get_item_model_cls().objects.filter(
                Q(**{m.get_region_field_attr(): selected_region, m.get_section_field_attr(): selected_section, item_target_field: 1}) |
                Q(**{'{0}__in'.format(m.get_identifier_field_attr()): identifiers, m.get_section_field_attr(): selected_section, item_target_field: 1}))
        icon = str(request.session['icon'])
        payload = m.prepare_map_points(items,
            icon,
            identifiers,
            'egg-circle',
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
            
        landmark_list = []
        landmarks = m.get_landmarks()
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        return render_to_response(
            template, {
                'region_field_attr': m.get_region_field_attr(),
                'section_field_attr': m.get_section_field_attr(),
                'mapper_name': mapper_name,
                'payload': payload,
                'action_script_url_name': action_script_url_name,
                'identifier_field_attr': m.get_identifier_field_attr(),
                'has_items': has_items,
                'mapper_item_label': mapper_item_label,
                'selected_region': selected_region,
                'selected_icon': request.session['icon'],
                'icons': m.get_icons(),
                'option': 'plot',
                'show_map': 1,
                'identifiers': identifiers,
                'landmarks': landmark_list,
                'cart_size': cart_size,
                'cso_icon_dict': cso_icon_dict,
                'section_color_code_list': section_color_code_list,
                'selected_section': selected_section
                },
                context_instance=RequestContext(request)
            )
