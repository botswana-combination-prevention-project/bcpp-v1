from django import forms

from edc.device.dispatch.forms import DispatchForm

from bhp066.apps.bcpp_survey.models import Survey


class BcppDispatchForm(DispatchForm):

    survey = forms.ModelChoiceField(
        queryset=Survey.objects.all().order_by('survey_name'),
        required=False)
