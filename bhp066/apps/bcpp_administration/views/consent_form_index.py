from django.shortcuts import render_to_response
from django.template import RequestContext
from ..forms import CorrectConsentForm


def consent_form_index(request, **kwargs):
    """Clears all sections for a given region."""

    template = 'correct_consent_form.html'
    correct_consent_form = CorrectConsentForm
    return render_to_response(
            template, {
                'correct_consent_form': correct_consent_form,
             },
            context_instance=RequestContext(request)
        )
