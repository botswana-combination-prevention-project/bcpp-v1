from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models.loading import get_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from ..models import PlotLog


@login_required
def create_plot_log(request):
    instance = None
    plot_pk = request.GET.get('plot')
    plot = get_model('bcpp_household', 'Plot').objects.get(pk=plot_pk)
    # only allow a PlotLog to be created when the user tries
    # by hitting the link.
    try:
        instance = PlotLog.objects.get(plot=plot)
    except PlotLog.DoesNotExist:
        try:
            instance = PlotLog.objects.create(plot=plot)
        except ValidationError as validation_error:
            # specifically looking for validation error from
            # allow enrollment method on the model
            messages.add_message(
                request, messages.ERROR,
                str(validation_error).replace(
                    'This plot', 'Plot {}'.format(plot.plot_identifier))
            )
            instance = None
    if instance:
        url = plot.log_entry_form_urls
        _, entry_url = url.popitem()
        url_link = entry_url + "?plot_log=" + instance.pk + "&next=/bcpp/section/plot/"
    else:
        url_link = '/bcpp/section/plot/'
    return HttpResponseRedirect(url_link)
