from django.db.models.loading import get_model
from django.http import HttpResponseRedirect

from ..models import PlotLog


def create_plot_log(request):
    instance = None
    plot_pk = request.GET.get('plot')
    plot = get_model('bcpp_household', 'Plot').objects.get(pk=plot_pk)
    try:
        instance = PlotLog.objects.get(plot=plot)
    except PlotLog.DoesNotExist:
        instance = PlotLog.objects.create(
            plot=plot
            )
    url = plot.log_entry_form_urls
    key, entry_url = url.popitem()
    url_link = entry_url + "?plot_log=" + instance.pk + "&next=/bcpp/section/plot/"
    return HttpResponseRedirect(url_link)
