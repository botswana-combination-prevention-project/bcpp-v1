from django import forms
from datetime import datetime 
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner, QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, HivHealthCareCosts, LabourMarketWages, Grant, BaselineHouseholdSurvey, CeaEnrolmentChecklist, CsEnrolmentChecklist, ResidencyMobility, Demographics, CommunityEngagement, Education, HivTestingHistory, HivTestReview, HivTestingSupplemental, SexualBehaviour, MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner, HivCareAdherence, HivMedicalCare, Circumcision, Circumcised, Uncircumcised, ReproductiveHealth, MedicalDiagnoses, SubstanceUse, Stigma, StigmaOpinion, PositiveParticipant, AccessToCare, HouseholdComposition, Respondent 


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
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating marital status
        if cleaned_data['maritalstatus'] == 'Married' and not cleaned_data['numwives']:
            raise forms.ValidationError('If participant is married, give number of wives')
        cleaned_data = super(DemographicsForm, self).clean()
        return cleaned_data
    
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
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating when testing declined
        if cleaned_data['HHhivtest'] == 'Declined' and not cleaned_data['whynohivtest']:
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing (2)')
        cleaned_data = super(HivTestingHistoryForm, self).clean()
        return cleaned_data


    class Meta:
        model = HivTestingHistory


#HivTestReview
class HivTestReviewForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        #to ensure that HIV test date is not greater than today
        if cleaned_data.get('hivtestdate'):
            if cleaned_data.get('hivtestdate') > datetime.today():
                raise forms.ValidationError('The last recorded HIV test date cannot be greater than today\'s date. Please correct.')
        
        return super(HivTestReviewForm, self).clean()

    class Meta:
        model = HivTestReview


#HivTestingSupplemental
class HivTestingSupplementalForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating a need to specify the participant's preference 
        if cleaned_data['hivtest_time'] == 'Yes, specify' and not cleaned_data['hivtest_time_other']:
            raise forms.ValidationError('If participant prefers a different test date/time than what is indicated, indicate the preference.')
        
        if cleaned_data['hivtest_week'] == 'Yes, specify' and not cleaned_data['hivtest_week_other']:
            raise forms.ValidationError('If participant has preference for testing on a particular day of the week, indicate the preference.')
        
        if cleaned_data['hivtest_year'] == 'Yes, specify' and not cleaned_data['hivtest_year_other']:
            raise forms.ValidationError('If participant prefers time of the year than the options given, indicate the preference.')
        cleaned_data = super(HivTestingSupplementalForm, self).clean()
        return cleaned_data
    
    class Meta:
        model = HivTestingSupplemental


#SexualBehaviour
class SexualBehaviourForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #if respondent has had sex, answer all following questions on form
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['lastyearpartners']:
            raise forms.ValidationError('If participant has had sex, how many people has he/she had sex with')
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['moresex']:
            raise forms.ValidationError('If participant has had sex, we need to know if this person lives outside community')
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['firstsex']:
            raise forms.ValidationError('If participant has had sex, how old was he/she when he/she first had sex')
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['condom']:
            raise forms.ValidationError('If participant has had sex, was a condom used the last time he/she had sex?')
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['alcohol_sex']:
            raise forms.ValidationError('If participant has had sex, did he/she or partner have alcohol?')
        if cleaned_data['eversex'] == 'Yes' and not cleaned_data['lastsex']:
            raise forms.ValidationError('If participant has had sex, when was the last time he/she had sex?')
        if cleaned_data['lastsex'] == 'Days' and not cleaned_data['lastsex_calc']:
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of days')
        if cleaned_data['lastsex'] == 'Months' and not cleaned_data['lastsex_calc']:
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of months')
        if cleaned_data['lastsex'] == 'Years' and not cleaned_data['lastsex_calc']:
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of years')
        
        cleaned_data = super(SexualBehaviourForm, self).clean()
        return cleaned_data

    class Meta:
        model = SexualBehaviour
        

#MonthsRecentPartner
class MonthsRecentPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data['firstpartnerhiv'] == 'negative' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data['firstpartnerhiv'] == 'I am not sure' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        cleaned_data = super(MonthsRecentPartnerForm, self).clean()
        return cleaned_data

    class Meta:
        model = MonthsRecentPartner


# MonthsSecondPartner
class MonthsSecondPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data['firstpartnerhiv'] == 'negative' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data['firstpartnerhiv'] == 'I am not sure' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        cleaned_data = super(MonthsSecondPartnerForm, self).clean()

        return cleaned_data

    class Meta:
        model = MonthsSecondPartner


# MonthsThirdPartner
class MonthsThirdPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data['firstpartnerhiv'] == 'negative' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data['firstpartnerhiv'] == 'I am not sure' and cleaned_data['firsthaart'] == 'Yes' or cleaned_data['firsthaart'] == 'No' or cleaned_data['firsthaart'] == 'not sure' or cleaned_data['firsthaart'] == 'Don\'t want to answer':
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        cleaned_data = super(MonthsThirdPartnerForm, self).clean()

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


#ReproductiveHealth
class ReproductiveHealthForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = ReproductiveHealth


#MedicalDiagnoses
class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = MedicalDiagnoses


#SubstanceUse
class SubstanceUseForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = SubstanceUse


#Stigma
class StigmaForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = Stigma


#StigmaOpinion
class StigmaOpinionForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = StigmaOpinion


#PositiveParticipant
class PositiveParticipantForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = PositiveParticipant


#AccessToCare
class AccessToCareForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = AccessToCare


# HouseholdComposition
class HouseholdCompositionForm (BaseSubjectModelForm):

    class Meta:
        model = HouseholdComposition


# Respondent
class RespondentForm (BaseSubjectModelForm):

    class Meta:
        model = Respondent
