from edc.base.form.forms import BaseModelForm
from apps.bcpp_list.models import (ElectricalAppliances, TransportMode, LiveWith,
                              NeighbourhoodProblems, CircumcisionBenefits,
                              FamilyPlanning, MedicalCareAccess, PartnerResidency,
                              HeartDisease, Diagnoses, Religion, EthnicGroups,
                              ReferredTo, ReferredFor, StiIllnesses)


class ElectricalAppliancesForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = ElectricalAppliances


class TransportModeForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = TransportMode


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


#CircumcisionBenefits
class CircumcisionBenefitsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = CircumcisionBenefits


#FamilyPlanning
class FamilyPlanningForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = FamilyPlanning


#MedicalCareAccess
class MedicalCareAccessForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = MedicalCareAccess


class PartnerResidencyForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = PartnerResidency


class HeartDiseaseForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HeartDisease


class DiagnosesForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Diagnoses


class ReligionForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Religion


class EthnicGroupsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = EthnicGroups


class ReferredForForm (BaseModelForm):

    class Meta:
        model = ReferredFor


class ReferredToForm (BaseModelForm):

    class Meta:
        model = ReferredTo


class StiIllnesses (BaseModelForm):

    class Meta:
        model = StiIllnesses
