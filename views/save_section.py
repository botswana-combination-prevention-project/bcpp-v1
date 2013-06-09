# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_household.models import Household
from mochudi_map.helpers import get_regions, get_icons


def save_section(request):
    """Assigns selected houselholds to the choosen ward section and save to database.

    for selected households by a polygon save the selected section to the ward_section
    field for each household
    """
    selected_section = request.GET.get('section')
    selected_region = request.GET.get('region')
   
    message = ""
    is_error = False
    household_identifiers = None
    identifiers = []
    payload = []
    ids = request.GET.get('household_identifiers')
    if ids:
        household_identifiers = ids.split(",")
    households = Household.objects.filter(household_identifier__in=household_identifiers)
    if household_identifiers:
        households = Household.objects.filter(household_identifier__in=household_identifiers)
        for household in households:
            household.ward_section = selected_section
            household.save()

        households = Household.objects.filter(ward=selected_region, ward_section__isnull=True)

    for household in households:
        payload.append([household.lon, household.lat, str(household.household_identifier), 'mark'])

    return render_to_response(
            'map_section.html', {
                'payload': payload,
                'identifiers': identifiers,
                'regions': get_regions(),
                'selected_section': selected_section,
                'selected_region': selected_region,
                'message': message,
                'option': 'save',
                'icons': get_icons(),
                'is_error': is_error,
                'show_map': 0
            },
            context_instance=RequestContext(request)
        )
