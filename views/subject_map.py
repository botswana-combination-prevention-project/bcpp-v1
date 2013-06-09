# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from mochudi_household.choices import MOCHUDI_LANDMARKS


def subject_map(request):
    """Displays map for a subject on the dashboard

        Show the location visually on the map of a subject from the dash by clicking the view map button
        on the dashboard
    """

    longitude = request.POST.get('lon')
    latitude = request.POST.get('lat')
    identifier = request.POST.get('identifier')
    
    landmarks = []
    landmark = MOCHUDI_LANDMARKS
    for place, lon, lat in landmark:
        landmarks.append([place, lon, lat])

    return render_to_response(
            'subject_map_location.html', {
                'latitude': latitude,
                'longitude': longitude,
                'landmarks': landmarks,
                'identifier': identifier
            },
            context_instance=RequestContext(request)
        )
