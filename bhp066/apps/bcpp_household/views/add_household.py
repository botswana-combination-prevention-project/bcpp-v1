from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import Household, Plot


def add_household(request, **kwargs):
    message = ''
    plot_identifier = kwargs.get('plot')
    plot = None
    if Plot.objects.filter(plot_identifier=plot_identifier, action='confirmed'):
        plot = Plot.objects.get(plot_identifier=plot_identifier, action='confirmed')
        plot.num_household += 1
        plot.save()
    else:
        message = 'Plot {0} has not been confirmed. You cannot add a household to an unconfirmed plot.'.format(plot.plot_identifier)
    households = Household.objects.filter(plot__plot_identifier=plot_identifier).order_by('household_identifier')
    household_meta = Household._meta
    return render_to_response(
        'add_household.html', {
            'households': households,
            'plot_identifier': plot_identifier,
            'plot': plot,
            'household_meta': household_meta,
            'message': message
            }, context_instance=RequestContext(request))
