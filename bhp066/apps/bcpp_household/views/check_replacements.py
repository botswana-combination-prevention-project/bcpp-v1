from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Min

from apps.bcpp_survey.models import Survey

from ..helpers import ReplacementHelper


def check_replacements(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    template = 'check_replacements.html'
    replacebles = []
    message = None
    producer_name = None
    if request.POST.get('producer_name'):
        producer_name = request.POST.get('producer_name')
        print producer_name
        first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
        survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
        replacement_households = ReplacementHelper().replaceable_households(survey, producer_name)
        replacement_plots = ReplacementHelper().replaceable_plots(producer_name)
        if replacement_households and replacement_plots:
            replacebles = replacement_households + replacement_plots
        elif replacement_households and not replacement_plots:
            replacebles = replacement_households
        elif not replacement_households and replacement_plots:
            replacebles = replacement_plots
    if not replacebles:
        message = "There are no replaceble households and plots form producer " + str(producer_name)
    return render_to_response(
            template, {
                'replacebles': replacebles,
                'replacement_count': len(replacebles),
                'producer_name': producer_name,
                'message': message,
                },
                context_instance=RequestContext(request)
            )
