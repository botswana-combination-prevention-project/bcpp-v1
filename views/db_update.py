from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from mochudi_household.models import Household
from math import sin, cos, radians, degrees, acos

def calc_dist(lat_a, long_a, lat_b, long_b):
    """Calculate distance between two geographic points
    
        Using latitude and longitude of two points calculate distance between points
        and return the distance in miles.
    """
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09


def db_update(request):
    """Updates coordinates of an entered household identifier
    
         Filter households by entered household then save the new coordinates of that household    
    """
    mochudi_center_lat = -24.376534
    mochudi_center_lon = 26.152276
    mochudi_radius = 8.699197
    
    template = "db_update.html"
    item_model_cls = Household
    #item_identifier_field = 'household_identifier'    
    identifier = request.POST.get('identifier')
    gps_s = request.POST.get('gps_s')
    longitude = request.POST.get('lon')
    
    gps_e = request.POST.get('gps_e')
    latitude = request.POST.get('lat')
    
    
    items = item_model_cls.objects.filter(household_identifier=identifier)
        
    if gps_s and longitude:
        gps_s = float(gps_s)
        longitude = float(longitude)
        
        lon = round((gps_s) + (longitude / 60), 5)
    
    if gps_e and latitude:
        gps_e = float(gps_e)
        latitude = float(latitude)
        
        lat = -1 * round((gps_e) + (latitude / 60), 5)  
    
    for item in items:
        item.gps_point_1 = gps_e
        item.gps_point_11 = latitude
        
        
        item.gps_point_2 = gps_s
        item.gps_point_21 = longitude
        
        
        distance = calc_dist(lat, lon, mochudi_center_lat, mochudi_center_lon)
        
        if distance <= mochudi_radius:
            item.save()
        else:               
            return HttpResponse("The coordinates you entered are outside mochudi, check if you have made errors.")
    
    return render_to_response(
                template,
            context_instance=RequestContext(request)
        )
