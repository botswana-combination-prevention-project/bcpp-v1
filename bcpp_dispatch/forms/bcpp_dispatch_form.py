from django import forms
from bhp_dispatch.forms import DispatchForm
from bcpp_survey.models import Survey


class BcppDispatchForm(DispatchForm):

    survey = forms.ModelChoiceField(
        queryset=Survey.objects.all().order_by('survey_name'),
        required=False)
