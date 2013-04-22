from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner, QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, HivHealthCareCosts, LabourMarketWages, Grant, BaselineHouseholdSurvey, CeaEnrolmentChecklist, CsEnrolmentChecklist, ResidencyMobility, Demographics, CommunityEngagement, Education, HivTestingHistory, HivTestReview, HivTestingSupplemental, SexualBehaviour, MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner, HivCareAdherence, HivMedicalCare, Circumcision, Circumcised, Uncircumcised 


# SubjectLocator
class SubjectLocatorForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectLocator


# SubjectDeath
class SubjectDeathForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectDeath


#RecentPartner
class RecentPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = RecentPartner


# SecondPartner
class SecondPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = SecondPartner


# ThirdPartner
class ThirdPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = ThirdPartner


# QualityOfLife
class QualityOfLifeForm (BaseSubjectModelForm):

    class Meta:
        model = QualityOfLife


# ResourceUtilization
class ResourceUtilizationForm (BaseSubjectModelForm):

    class Meta:
        model = ResourceUtilization


# OutpatientCare
class OutpatientCareForm (BaseSubjectModelForm):

    class Meta:
        model = OutpatientCare


# HospitalAdmission
class HospitalAdmissionForm (BaseSubjectModelForm):

    class Meta:
        model = HospitalAdmission


# HivHealthCareCosts
class HivHealthCareCostsForm (BaseSubjectModelForm):

    class Meta:
        model = HivHealthCareCosts


# LabourMarketWages
class LabourMarketWagesForm (BaseSubjectModelForm):

    class Meta:
        model = LabourMarketWages


# Grant
class GrantForm (BaseSubjectModelForm):

    class Meta:
        model = Grant


# BaselineHouseholdSurvey
class BaselineHouseholdSurveyForm (BaseSubjectModelForm):

    class Meta:
        model = BaselineHouseholdSurvey


# CeaEnrollmentChecklist
class CeaEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CeaEnrolmentChecklist


#CsEnrolmentChecklist
class CsEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CsEnrolmentChecklist


#ResidencyMobility
class ResidencyMobilityForm (BaseSubjectModelForm):

    class Meta:
        model = ResidencyMobility


#Demographics
class DemographicsForm (BaseSubjectModelForm):

    class Meta:
        model = Demographics


#CommunityEngagement
class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement


#Education
class EducationForm (BaseSubjectModelForm):

    class Meta:
        model = Education


#HivTestingHistory
class HivTestingHistoryForm (BaseSubjectModelForm):

    class Meta:
        model = HivTestingHistory


#HivTestReview
class HivTestReviewForm (BaseSubjectModelForm):

    class Meta:
        model = HivTestReview


#HivTestingSupplemental
class HivTestingSupplementalForm (BaseSubjectModelForm):

    class Meta:
        model = HivTestingSupplemental


#SexualBehaviour
class SexualBehaviourForm (BaseSubjectModelForm):

    class Meta:
        model = SexualBehaviour
        

#MonthsRecentPartner
class MonthsRecentPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = MonthsRecentPartner


# MonthsSecondPartner
class MonthsSecondPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = MonthsSecondPartner


# MonthsThirdPartner
class MonthsThirdPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = MonthsThirdPartner



#HivCareAdherence
class HivCareAdherenceForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = HivCareAdherence
        

#HivMedicalCare
class HivMedicalCareForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = HivMedicalCare
        

#Circumcision
class CircumcisionForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Circumcision
        

#Circumcised
class CircumcisedForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Circumcised


#Uncircumcised
class UncircumcisedForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Uncircumcised


