from django.views.generic import View
from django.shortcuts import render

from edc_quota import Override


class GenerateConfirmationKeyView(View):

    def __init__(self):
        self.template_name = 'generate_confirmation_key.html'

    def get_context_data(self, request, **kwargs):
        self.context = {}
        confirmation_code = self.create_confirmation_code(request.POST.get('override_key', ''))
        self.context.update({'override_key': request.POST.get('override_key', '')})
        self.context.update({'confirmation_code': confirmation_code})
        return self.context

    def post(self, request, *args, **kwargs):
        """Allows a POST -- without the class returns a 405 error."""
        return render(request, self.template_name, self.get_context_data(request, **kwargs))

    def get(self, request, *args, **kwargs):
        """Allows a GET -- without the class returns a 405 error."""
        return render(request, self.template_name, {})

    def create_confirmation_code(self, override_code):
        return Override().make_confirmation_code(override_code)[1]
