from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Min

from apps.bcpp_survey.models import Survey

from ..helpers import ReplacementHelper


def replace_data(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    template = 'replacement_data.html'
    replacebles = []
    first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
    survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
    replacement_households = ReplacementHelper().replaceable_households(survey)
    replacement_plots = ReplacementHelper().replaceable_plots()
    if replacement_households and replacement_plots:
        replacebles = replacement_households + replacement_plots
    elif replacement_households and not replacement_plots:
        replacebles = replacement_households
    elif not replacement_households and replacement_plots:
        replacebles = replacement_plots
    return render_to_response(
            template, {
                'replacement_data': replacebles,
                'replacement_count': len(replacebles),
                },
                context_instance=RequestContext(request)
            )
