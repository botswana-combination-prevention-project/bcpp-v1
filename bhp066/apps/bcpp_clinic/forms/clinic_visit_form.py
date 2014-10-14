from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from ..models import ClinicVisit
from apps.clinic.choices import VISIT_REASON

from edc.subject.consent.forms import BaseConsentedModelForm


class ClinicVisitForm (BaseConsentedModelForm):

    reason = forms.ChoiceField(
        label='Reason for clinic visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = ClinicVisit
