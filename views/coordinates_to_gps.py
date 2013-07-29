import os
# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError



def coordinates_to_gps(request, **kwargs):
    """Create a .gpx file to store coordinates in the GPS receiver to guide to a location.
    
    fname: is an already existing file
    """
    FNAME = 'Current.gpx'
    file_to_gps = '/Volumes/GARMIN/GPX/Current.gpx'
    
    f = open(FNAME, 'r')
    line = f.readline()
    lines = f.read()
    f.close()
    
    
    try:
        os.remove(file_to_gps)
    except OSError:
        pass
    wf = open(file_to_gps, 'a')
    wf.write(line)

    template = 'sent.html'
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')

    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        m = site_mappers.get_registry(mapper_name)()
        
        #This values need to come from the edc   
        items = m.get_item_model_cls().objects.all()
        for item in item:
            identifier_name = item.get_identifier_field_attr()
            lat = item.lat 
            lon = item.lon
            ele = 0.0
            city_village = item.get_map_area()
        
            str_from_edc = '<name>' + identifier_name +'</name><sym>Waypoint</sym><extensions><gpxx:WaypointExtension><gpxx:Categories><gpxx:Category>Map Points and Coordinates</gpxx:Category></gpxx:Categories><gpxx:Address><gpxx:City>'
            + city_village + '</gpxx:City><gpxx:State>South Eastern</gpxx:State></gpxx:Address></gpxx:WaypointExtension></extensions>' + '</wpt>' + '<wpt lat="' + lat + '" lon="' + lon + '"><ele>' + ele + '</ele>'
            
            #write to gps file from database
            wf.write(str_from_edc)
        wf.write(lines)
        wf.close()
    return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'file_to_gps': os.path.exists(file_to_gps)
            },
            context_instance=RequestContext(request)
        ) 
        
        
        