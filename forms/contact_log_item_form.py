from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from bhp_base_form.classes import BaseModelForm
from bhp_contact.forms import BaseContactLogItemFormCleaner
from bhp_contact.choices import CONTACT_TYPE, INFO_PROVIDER
from bhp_appointment.models import ContactLogItem


class ContactLogItemForm (BaseModelForm):

    contact_type = forms.ChoiceField(
        label='Contact type',
        choices=[choice for choice in CONTACT_TYPE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
        )
    information_provider = forms.ChoiceField(
        label="Person completing interview",
        choices=[choice for choice in INFO_PROVIDER],
        required=False,
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data = BaseContactLogItemFormCleaner().clean(cleaned_data)
        return super(ContactLogItemForm, self).clean()

    class Meta:
        model = ContactLogItem
