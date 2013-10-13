from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import Plot, Household


def add_household_index(request, **kwargs):
    """Allows to add household in a plot."""
    template = 'add_household.html'
    plot_identifier = kwargs.get('plot')
    message = ""
    plot = Plot.objects.filter(plot_identifier=plot_identifier)
    households = Household.objects.filter(plot__plot_identifier=plot_identifier).order_by('household_identifier')
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
