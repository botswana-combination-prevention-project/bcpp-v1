import os
# Import django modules
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError



def coordinates_to_gps(request, **kwargs):
    """Create a .gpx file to store coordinates in the GPS receiver to guide to a location.
    
    fname: is an already existing file
    """
    template = 'sent.html'
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')

    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        m = site_mappers.get_registry(mapper_name)()
        
        if settings.DEVICE_ID == '99':
            raise MapperError('You are in the server, You can\'t dispatch the whole server data to a GPS receiver.')
        else:    
            FNAME = '/users/django/source/bhp066/bhp_map/static/gpx/Current.gpx'
            f = open(FNAME, 'r')
            line = f.readline()
            lines = f.read()
            f.close()
            GPS_FILE_PATH = '/Volumes/GARMIN/GPX/Current.gpx'
            
        
    
            wf = open('/Volumes/GARMIN/GPX/Current.gpx', 'a')
            wf.write(line)
            
            
            #This values need to come from the edc   
            items = m.get_item_model_cls().objects.all()
            for item in items:
                identifier_name = str(getattr(item, m.get_identifier_field_attr()))
                lat = item.gps_target_lat 
                lon = item.gps_target_lon
                ele = 0.0
                city_village = m.get_map_area()
                str_from_edc = '<wpt lat="' + str(lat) + '" lon="' + str(lon) + '"><ele>' + str(ele) + '</ele>' + '<name>' + str(identifier_name) + '</name><sym>Waypoint</sym><extensions><gpxx:WaypointExtension><gpxx:Categories><gpxx:Category>Map Points and Coordinates</gpxx:Category></gpxx:Categories><gpxx:Address><gpxx:City>' + str(city_village) + '</gpxx:City><gpxx:State>South Eastern</gpxx:State></gpxx:Address></gpxx:WaypointExtension></extensions>' + '</wpt>'
                print str_from_edc
                wf.write(str_from_edc)
            wf.write(lines)
            wf.close()
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'file_to_gps': GPS_FILE_PATH
                },
                context_instance=RequestContext(request)
            )
        
        
