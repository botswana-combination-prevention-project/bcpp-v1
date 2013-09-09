# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def item_map(request, **kwargs):
    """Displays map for a subject on the dashboard

        Show the location visually on the map of a subject from the dash by clicking the view map button
        on the dashboard
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        longitude = kwargs.get('lon', None)
        latitude = kwargs.get('lat', None)
        if not longitude:
            raise MapperError('Attribute longitude may not be None. Got {0}'.format(kwargs))
        if not latitude:
            raise MapperError('Attribute latitude may not be None. Got {0}'.format(kwargs))
       
        identifier = kwargs.get('identifier', None)
        landmark_list = []
        landmarks = m.get_landmarks()
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        return render_to_response(
                'item_map_location.html', {
                    'latitude': latitude,
                    'mapper_name': mapper_name,
                    'longitude': longitude,
                    'landmarks': landmark_list,
                    'identifier': identifier
                },
                context_instance=RequestContext(request)
            )
