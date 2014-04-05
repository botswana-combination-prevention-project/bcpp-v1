from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.device.sync.models import Producer


def replacement_index(request, **kwargs):
    """Clears all sections for a given region."""

    template = 'replacement_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    producers = Producer.objects.all()
    producer_names = []
    message = ''
    for producer in producers:
        producer_names.append(producer.name)
    if not producer_names:
        message = 'Add producers to your producer table'
    return render_to_response(
            template, {
                'message': message,
                'producer_names': producer_names,
             },
            context_instance=RequestContext(request)
        )
