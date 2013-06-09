# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from mochudi_household.models import Household
from mochudi_map.choices import ICONS
from mochudi_map.helpers import prepare_map_points, get_sections, make_dictionary, get_icons, get_other_icons


def plot_item_points(request):
    """Plot households from base selection criteria.

    Filter points to plot by sending coordinates of a selected ward only to the households.html template.


    Regions contain sections    """
    # TODO: difference in ward ward section selected section and section ??? very confusing
            # docstring Comment is out of date?
    template = 'map.html'
    item_model_cls = Household
    item_identifier_field = 'household_identifier'
    item_region_field = 'ward'
    item_section_field = 'ward_section'
    item_target_field = 'target'
    action_script_url = '/mochudi_map/add_cart/?household_identifiers='
    # get_region_list = get_wards_list

    has_items = False
    item_label = item_model_cls._meta.object_name
    identifiers = request.session.get('identifiers', [])
    selected_section = request.POST.get('section')
    cart_size = len(identifiers)
    cso_icon_dict = []
    section_color_code_list = []
    # sections = [None]  # TODO: what's this??
    selected_region = request.POST.get(item_region_field)  # TODO: this should not be "ward" on the template
    request.session['icon'] = request.POST.get('marker_icon')
    if selected_section == 'All':
        items = item_model_cls.objects.filter(
            Q(**{item_region_field: selected_region, item_target_field: 1}) |
            Q(**{'{0}__in'.format(item_identifier_field): identifiers}))
    else:
        items = item_model_cls.objects.filter(
            Q(**{item_region_field: selected_region, item_section_field: selected_section, item_target_field: 1}) |
            Q(**{'{0}__in'.format(item_identifier_field): identifiers, item_section_field: selected_section, item_target_field: 1}))
    icon = str(request.session['icon'])
    print selected_section
    payload = prepare_map_points(items,
        icon,
        identifiers,
    'mark', 'red-circle', selected_section)

    if selected_section != "ALL":
        for lon, lat, label, icon, cso in payload:
            icon_name_length = len(icon)
            icon_label = icon[icon_name_length-1]
            #print icon_label
            cso_icon_dict.append([icon_label,cso])
        
    if selected_section == "All":
        section_color_codes = make_dictionary(get_other_icons(), get_sections())
    else:
        section_color_codes = make_dictionary(get_icons(), get_sections())
    
    for key_color, sec_value in section_color_codes.iteritems():
        section_color_code_list.append([key_color[:-1], sec_value])
    
    if payload:
        has_items = True
    return render_to_response(
        template, {
            'payload': payload,
            #'sections': sections,  # TODO: what does this do?? is always [] and does not appear ofn the template.
            'action_script_url': action_script_url,
            #'regions': get_region_list(),  # seems to not do anything, not on template
            'has_items': has_items,
            'item_label': item_label,
            'selected_region': selected_region,
            'selected_icon': request.session['icon'],
            'icons': ICONS,
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
