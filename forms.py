from django import forms
from bhp_base_form.forms import BaseModelForm
from lab_barcode.models import ZplTemplate, LabelPrinter


class LabelForm(forms.Form):

    identifier = forms.CharField(
        max_length=25,
        label="Identifier",
        help_text="",
        error_messages={'required': 'Please enter a valid identifier.'},
        #initial=""
        )


class ZplTemplateForm (BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = ZplTemplate


class LabelPrinterForm (BaseModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = LabelPrinter
