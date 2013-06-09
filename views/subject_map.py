# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def subject_map(request):
    """Displays map for a subject on the dashboard

        Show the location visually on the map of a subject from the dash by clicking the view map button
        on the dashboard
    """
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        longitude = request.POST.get('lon')
        latitude = request.POST.get('lat')
        identifier = request.POST.get('identifier')
        landmark_list = []
        landmarks = m.get_landmarks()
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        return render_to_response(
                'subject_map_location.html', {
                    'latitude': latitude,
                    'longitude': longitude,
                    'landmarks': landmark_list,
                    'identifier': identifier
                },
                context_instance=RequestContext(request)
            )
