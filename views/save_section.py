# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError
from bhp_map.utils import get_longitude, get_latitude


def save_section(request):
    """Assigns selected houselholds to the choosen ward section and save to database.

    for selected households by a polygon save the selected section to the ward_section
    field for each household
    """
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        selected_section = request.GET.get('section')
        selected_region = request.GET.get('region')
        message = ""
        is_error = False
        item_identifiers = None
        item_identifiers = []
        payload = []
        item_identifiers = request.GET.get('household_identifiers')
        if item_identifiers:
            item_identifiers = item_identifiers.split(",")
        items = []
        if item_identifiers:
            items = m.get_item_model_cls().objects.filter(**{'{0}__in'.format(m.item_identifier_field_attr): item_identifiers})
            #households = Household.objects.filter(household_identifier__in=household_identifiers)
            for item in items:
                setattr(item, m.section_field_attr, selected_section)
                item.save()
            items = m.get_item_model_cls().objects.filter(**{m.region_field_attr: selected_region, '{0}__isnull'.format(m.section_field_attr): True})
        for item in items:
            lon = get_longitude(getattr(item, m.gps_s_field_attr), getattr(item, m.gps_longitude_field_attr))
            lat = get_latitude(getattr(item, m.gps_e_field_attr), getattr(item, m.gps_latitude_field_attr))
            payload.append([lon, lat, str(getattr(item, m.identifier_field_attr)), 'mark'])
        return render_to_response(
                'map_section.html', {
                    'payload': payload,
                    'identifiers': item_identifiers,
                    'regions': m.get_regions(),
                    'selected_section': selected_section,
                    'selected_region': selected_region,
                    'message': message,
                    'option': 'save',
                    'icons': m.get_icons(),
                    'is_error': is_error,
                    'show_map': 0
                },
                context_instance=RequestContext(request)
            )
