from bhp_base_form.classes import BaseModelForm
from bcpp_list.models import ElectricalAppliances, TransportMode


# ElectricalAppliances
class ElectricalAppliancesForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = ElectricalAppliances


# TransportMode
class TransportModeForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = TransportMode
