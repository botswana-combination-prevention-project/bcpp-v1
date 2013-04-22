from bhp_base_form.classes import BaseModelForm
from bcpp_list.models import ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems, CicumcisionBenefits


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


# LiveWith
class LiveWithForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = LiveWith


#NeighbourhoodProblems
class NeighbourhoodProblemsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = NeighbourhoodProblems


#CicumcisionBenefits
class CicumcisionBenefitsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = CicumcisionBenefits
