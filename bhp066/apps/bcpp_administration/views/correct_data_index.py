from django.shortcuts import render_to_response
from django.template import RequestContext


def correct_data_index(request, **kwargs):
    """Goes to the pages to choose data to correct."""

    template = 'correct_data_index.html'
    return render_to_response(
            template, {

             },
            context_instance=RequestContext(request)
        )
