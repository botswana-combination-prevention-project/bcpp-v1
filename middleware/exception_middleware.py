from django.shortcuts import render_to_response
from django.template import RequestContext


class ExceptionMiddleware(object):

    def process_exception(self, request, exception):

        return render_to_response(
            'exception.html',
            {'exception': exception},
            context_instance=RequestContext(request))
