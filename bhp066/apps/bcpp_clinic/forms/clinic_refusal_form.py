from edc.base.form.forms import BaseModelForm

from ..models import ClinicRefusal


class ClinicRefusalForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicRefusalForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicRefusal
