from edc.core.bhp_base_form.forms import BaseModelForm
from ..models import Plot


class PlotForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Plot
