from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import (SubjectLocator, SubjectDeath, QualityOfLife, 
                                 ResourceUtilization, OutpatientCare, HospitalAdmission,
                                 HivHealthCareCosts, LabourMarketWages, Grant,
                                 CeaEnrolmentChecklist, CsEnrolmentChecklist,
                                 CommunityEngagement, Education,
                                 HivMedicalCare, Circumcision, Circumcised,
                                 ReproductiveHealth, MedicalDiagnoses, HeartAttack,
                                 Cancer, Tubercolosis, SubstanceUse, Stigma, 
                                 StigmaOpinion, PositiveParticipant, 
                                 HouseholdComposition, Respondent, 
                                 HivResultDocumentation)


class SubjectLocatorForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectLocator


class SubjectDeathForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectDeath


class QualityOfLifeForm (BaseSubjectModelForm):

    class Meta:
        model = QualityOfLife


class ResourceUtilizationForm (BaseSubjectModelForm):

    class Meta:
        model = ResourceUtilization


class OutpatientCareForm (BaseSubjectModelForm):

    class Meta:
        model = OutpatientCare


class HospitalAdmissionForm (BaseSubjectModelForm):

    class Meta:
        model = HospitalAdmission


class HivHealthCareCostsForm (BaseSubjectModelForm):

    class Meta:
        model = HivHealthCareCosts


class LabourMarketWagesForm (BaseSubjectModelForm):

    class Meta:
        model = LabourMarketWages


class GrantForm (BaseSubjectModelForm):

    class Meta:
        model = Grant


class CeaEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CeaEnrolmentChecklist


class CsEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CsEnrolmentChecklist


class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement


class EducationForm (BaseSubjectModelForm):

    class Meta:
        model = Education


class HivMedicalCareForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = HivMedicalCare


class CircumcisionForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Circumcision


class CircumcisedForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Circumcised


class ReproductiveHealthForm (BaseSubjectModelForm):

    class Meta:
        model = ReproductiveHealth


class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = MedicalDiagnoses


class SubstanceUseForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = SubstanceUse


class StigmaForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Stigma


class StigmaOpinionForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = StigmaOpinion


class PositiveParticipantForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = PositiveParticipant


class HouseholdCompositionForm (BaseSubjectModelForm):

    class Meta:
        model = HouseholdComposition


class RespondentForm (BaseSubjectModelForm):

    class Meta:
        model = Respondent


class HeartAttackForm (BaseSubjectModelForm):

    class Meta:
        model = HeartAttack


class CancerForm (BaseSubjectModelForm):

    class Meta:
        model = Cancer


class TubercolosisForm (BaseSubjectModelForm):

    class Meta:
        model = Tubercolosis


class HivResultDocumentationForm (BaseSubjectModelForm):

    class Meta:
        model = HivResultDocumentation
