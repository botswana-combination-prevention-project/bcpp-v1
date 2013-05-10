from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from bhp_base_form.forms import BaseModelForm
from bhp_contact.forms import BaseContactLogItemFormCleaner
from bhp_appointment.models import PreAppointmentContact
from bhp_appointment.choices import INFO_PROVIDER


class PreAppointmentContactForm (BaseModelForm):

    information_provider = forms.ChoiceField(
        label='Who answered?',
        choices=[('', 'None')] + list(INFO_PROVIDER),
        required=False,
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        BaseContactLogItemFormCleaner().clean(cleaned_data)
        return super(PreAppointmentContactForm, self).clean()

    class Meta:
        model = PreAppointmentContact
