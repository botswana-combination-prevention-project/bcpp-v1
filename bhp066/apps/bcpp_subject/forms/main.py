from ..models import (SubjectDeath, QualityOfLife,
                                 ResourceUtilization, OutpatientCare, HospitalAdmission,
                                 HivHealthCareCosts, LabourMarketWages, Grant,
                                 HeartAttack, Cancer, Tubercolosis,
                                 Sti, SubstanceUse)
from .base_subject_model_form import BaseSubjectModelForm


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


class SubstanceUseForm (BaseSubjectModelForm):

    class Meta:
        model = SubstanceUse


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
