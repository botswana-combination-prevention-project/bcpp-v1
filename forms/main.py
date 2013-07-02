from bhp_base_form.forms import BaseModelForm
from bcpp_list.models import ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems, CircumcisionBenefits, FamilyPlanning, MedicalCareAccess, PartnerResidency


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

#HouseholdSurveyCode
#HouseholdSurveyReason
#HouseholdSurveySource
#SurveyGroup
#HouseholdStructureRelation
#HouseholdSurveyStatus
#SubjectAbsenteeReason
#SubjectMovedReason
