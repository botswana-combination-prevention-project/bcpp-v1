from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import Household, Plot

def add_household(request, **kwargs):
    
    template = 'add_household.html'
    message = ''
    plot_identifier = kwargs.get('plot')
    plot = Plot.objects.filter(plot_identifier=plot_identifier)
    if plot[0].action == 'confirmed':
        Household.objects.create(**{'plot': plot[0],
                                    'gps_target_lat': plot[0].gps_target_lat,
                                    'gps_target_lon': plot[0].gps_target_lon,
                                    'gps_lat': plot[0].gps_lat,
                                    'gps_lon': plot[0].gps_lon,
                                    'gps_degrees_e': plot[0].gps_degrees_e,
                                    'gps_degrees_s': plot[0].gps_degrees_s,
                                    'gps_minutes_e': plot[0].gps_minutes_e,
                                    'gps_minutes_s': plot[0].gps_minutes_s,
                                    })
    else:
        message = 'You cannot add a household on an unconfirmed plot'
    households = Household.objects.filter(plot__plot_identifier=plot_identifier).order_by('household_sequence')
    household_meta = Household._meta
    return render_to_response(
            template, {
                'households': households,
                'plot_identifier': plot_identifier,
                'plot': plot[0],
                'household_meta': household_meta,
                'message': message
                },
                context_instance=RequestContext(request)
            )