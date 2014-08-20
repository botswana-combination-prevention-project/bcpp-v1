from django.shortcuts import render_to_response
from django.template import RequestContext

from ..forms import PlotRadius


def increase_plot_radius(request):
    """Plot form for radius"""

    radius_form = PlotRadius
    template = 'plot_radius.html'
    return render_to_response(
            template, {
            "radius_form": radius_form,
             },
            context_instance=RequestContext(request)
        )
