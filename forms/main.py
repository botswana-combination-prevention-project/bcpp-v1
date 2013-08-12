from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import (SubjectLocator, SubjectDeath, QualityOfLife,
                                 ResourceUtilization, OutpatientCare, HospitalAdmission,
                                 HivHealthCareCosts, LabourMarketWages, Grant,
                                 CeaEnrolmentChecklist, CommunityEngagement,
                                 HivMedicalCare, MedicalDiagnoses, HeartAttack,
                                 Cancer, Tubercolosis, Sti, SubstanceUse, Stigma,
                                 StigmaOpinion, PositiveParticipant,
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


class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement


class HivMedicalCareForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = HivMedicalCare


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


class HeartAttackForm (BaseSubjectModelForm):

    class Meta:
        model = HeartAttack


class CancerForm (BaseSubjectModelForm):

    class Meta:
        model = Cancer


class TubercolosisForm (BaseSubjectModelForm):

    class Meta:
        model = Tubercolosis


class StiForm (BaseSubjectModelForm):

    class Meta:
        model = Sti


class HivResultDocumentationForm (BaseSubjectModelForm):

    class Meta:
        model = HivResultDocumentation
