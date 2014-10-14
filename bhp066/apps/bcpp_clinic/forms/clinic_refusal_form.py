from ..models import ClinicRefusal

from edc.base.form.forms import BaseModelForm


class ClinicRefusalForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicRefusalForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicRefusal
