# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def save_sub_section(request, **kwargs):
    """Assigns selected items to the chosen ward section and save to database.

    for selected items by a polygon save the selected section to the ward_section
    field for each item
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        #selected_section = request.GET.get('section')
        selected_region = request.GET.get(m.get_region_field_attr())
        selected_sub_section = request.GET.get(m.get_section_field_attr())
        message = ""
        is_error = False
        item_identifiers = None
        item_identifiers = []
        payload = []
        item_identifiers = request.GET.get('identifiers')
        if item_identifiers:
            item_identifiers = item_identifiers.split(",")
        items = []
        if item_identifiers:
            items = m.get_item_model_cls().objects.filter(**{'{0}__in'.format(m.identifier_field_attr): item_identifiers})
            for item in items:
                setattr(item, m.section_field_attr, selected_sub_section)
                item.save()
            items = m.get_item_model_cls().objects.filter(**{m.region_field_attr: selected_region, '{0}__isnull'.format(m.section_field_attr): True})
        for item in items:
            lon = item.gps_target_lon
            lat = item.gps_target_lat
            payload.append([lon, lat, str(getattr(item, m.identifier_field_attr)), 'mark'])
        return render_to_response(
                'map_section.html', {
                    'payload': payload,
                    'mapper_name': mapper_name,
                    'identifiers': item_identifiers,
                    'regions': m.get_regions(),
                    'selected_region': selected_region,
                    'selected_sub_section': selected_sub_section,
                    'message': message,
                    'option': 'save',
                    'icons': m.get_icons(),
                    'is_error': is_error,
                    'show_map': 0
                },
                context_instance=RequestContext(request)
            )
