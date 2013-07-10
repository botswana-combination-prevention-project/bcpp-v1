from django import forms
from datetime import datetime
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import (SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, 
                                 ThirdPartner, QualityOfLife, ResourceUtilization, 
                                 OutpatientCare, HospitalAdmission, 
                                 HivHealthCareCosts, LabourMarketWages, Grant,
                                 CeaEnrolmentChecklist, CsEnrolmentChecklist, 
                                 CommunityEngagement, Education,
                                 HivTestReview, HivTested, HivUntested, FutureHivTesting, 
                                 MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner, 
                                 HivMedicalCare, Circumcision, Circumcised, Uncircumcised, 
                                 ReproductiveHealth, MedicalDiagnoses, HeartAttack, Cancer, 
                                 Tubercolosis, SubstanceUse, Stigma, StigmaOpinion, 
                                 PositiveParticipant, AccessToCare, HouseholdComposition, 
                                 Respondent, TodaysHivResult, HivResultDocumentation)


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


# CeaEnrollmentChecklist
class CeaEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CeaEnrolmentChecklist


#CsEnrolmentChecklist
class CsEnrolmentChecklistForm (BaseSubjectModelForm):

    class Meta:
        model = CsEnrolmentChecklist


#CommunityEngagement
class CommunityEngagementForm (BaseSubjectModelForm):

    class Meta:
        model = CommunityEngagement


#Education
class EducationForm (BaseSubjectModelForm):

    class Meta:
        model = Education


#HivTestReview
class HivTestReviewForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        #to ensure that HIV test date is not greater than today
        if cleaned_data.get('hiv_test_date'):
            if cleaned_data.get('hiv_test_date') > datetime.today():
                raise forms.ValidationError('The last recorded HIV test date cannot be greater than today\'s date. Please correct.')
        
        return super(HivTestReviewForm, self).clean()

    class Meta:
        model = HivTestReview


# #HivTestingSupplemental
# class HivTestingSupplementalForm (BaseSubjectModelForm):
#     
#     def clean(self):
# 
#         cleaned_data = self.cleaned_data
#         
#         #if no, don't answer next question
#         if cleaned_data.get('hiv_pills') == 'No' and  cleaned_data.get('arvshivtest'):
#             raise forms.ValidationError('You are answering information about ARV\'s yet have answered \'NO\', patient has never heard about ARV\'s. Please correct')
#         if cleaned_data.get('hiv_pills') == 'Yes' or cleaned_data.get('hiv_pills') == 'not sure' and not cleaned_data.get('arvshivtest'):
#             raise forms.ValidationError('if "%s", answer whether participant believes that HIV positive can live longer if taking ARV\'s. (Q Supplemental HT6)')
#         
#         return cleaned_data
# 
#     class Meta:
#         model = HivTestingSupplemental



#HivTested
class HivTestedForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        if cleaned_data.get('num_hiv_tests') == 0:
            raise forms.ValidationError('if participant has tested before, number of HIV tests before today cannot be zero. Please correct')
        #if no, don't answer next question
        if cleaned_data.get('hiv_pills') == 'No' and  cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('You are answering information about ARV\'s yet have answered \'NO\', patient has never heard about ARV\'s. Please correct')
        if cleaned_data.get('hiv_pills') == 'Yes' or cleaned_data.get('hiv_pills') == 'not sure' and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('if "%s", answer whether participant believes that HIV positive can live longer if taking ARV\'s. (Q Supplemental HT6)')
         
        return cleaned_data

    class Meta:
        model = HivTested

      
#HivUntested
class HivUntestedForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data
         
        #if no, don't answer next question
        if cleaned_data.get('hiv_pills') == 'No' and  cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('You are answering information about ARV\'s yet have answered \'NO\', patient has never heard about ARV\'s. Please correct')
        if cleaned_data.get('hiv_pills') == 'Yes' or cleaned_data.get('hiv_pills') == 'not sure' and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('if "%s", answer whether participant believes that HIV positive can live longer if taking ARV\'s. (Q Supplemental HT6)')
         
        return cleaned_data

    class Meta:
        model = HivUntested


#MonthsRecentPartner
class MonthsRecentPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #ensuring that question about antiretrovirals is not answered if partner is known to be HIV negative
        if cleaned_data.get('firstpartnerhiv') == 'negative' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
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
        if cleaned_data.get('firstpartnerhiv') == 'negative' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
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
        if cleaned_data.get('firstpartnerhiv') == 'negative' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
            raise forms.ValidationError('Do not answer this question if partners HIV status is known to be negative')
        if cleaned_data.get('firstpartnerhiv') == 'I am not sure' and cleaned_data.get('firsthaart') == 'Yes' or cleaned_data.get('firsthaart') == 'No' or cleaned_data.get('firsthaart') == 'not sure' or cleaned_data.get('firsthaart') == 'Don\'t want to answer':
            raise forms.ValidationError('If partner status is not known, do not give information about status of ARV\'s')
        cleaned_data = super(MonthsThirdPartnerForm, self).clean()

        return cleaned_data

    class Meta:
        model = MonthsThirdPartner


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
        #validate other
        if cleaned_data.get('circumcision_day') and not cleaned_data.get('circumcision_day_other'):
            raise forms.ValidationError('if \'YES\', specify the day preferred.')
        if cleaned_data.get('circumcision_week') and not cleaned_data.get('circumcision_week_other'):
            raise forms.ValidationError('if \'YES\', specify the week preferred.')
        if cleaned_data.get('circumcision_year') and not cleaned_data.get('circumcision_year_other'):
            raise forms.ValidationError('if \'YES\', specify the year preferred.')

        return cleaned_data

    class Meta:
        model = Uncircumcised
        randomise = [('aware_free',14,[1,1,0,0,0,0,0,0,0,0])]


class ReproductiveHealthForm (BaseSubjectModelForm):
    
    class Meta:
        model = ReproductiveHealth
        
        

#MedicalDiagnoses
class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #Validating that heartattack info is not given if patient has never had a heartattach
#         if cleaned_data.get('heart_attack') == 'No' and cleaned_data.get('heart_attack_record') or cleaned_data.get('date_heart_attack') or cleaned_data.get('dx_heart_attack'):
#             raise forms.ValidationError('You are giving more heart_attack related information yet have answered \'NO\', to (Q86)')
#         #if patient has had heart attack, is summary in OPD
#         if cleaned_data.get('heart_attack') == 'Yes' and not cleaned_data.get('heart_attack_record'):
#             raise forms.ValidationError('if patient has had a heart attack, is there a record available on the OPD card?')
#         #if OPD record available, give date as on OPD
#         if cleaned_data.get('heart_attack_record') == 'Yes' and not cleaned_data.get('date_heart_attack'):
#             raise forms.ValidationError('If a record of the heart attack is available on the OPD card, give the date of diagnosis')
#         #if OPD record available, give diagnosis as recorded on OPD
#         if cleaned_data.get('heart_attack_record') == 'Yes' and not cleaned_data.get('dx_heart_attack'):
#             raise forms.ValidationError('If a record of the heart attack is available on the OPD card, provide the diagnosis detail (Q89).')
#         
#         #Validating that cancer info is not given if patient has never been diagnosed with cancer
#         if cleaned_data.get('cancer') == 'No' and cleaned_data.get('cancer_record') or cleaned_data.get('date_cancer') or cleaned_data.get('dx_cancer'):
#             raise forms.ValidationError('You are giving more cancer related information yet have answered \'NO\',patient has never been told he/she has cancer to (Q90)')
#         #if patient has had cancer, is summary in OPD
#         if cleaned_data.get('cancer') == 'Yes' and not cleaned_data.get('cancer_record'):
#             raise forms.ValidationError('if patient has cancer, is there a cancer record available on the OPD card?')
#         if cleaned_data.get('cancer_record') == 'Yes' and not cleaned_data.get('date_cancer'):
#             raise forms.ValidationError('if cancer record is available on the OPD card, what is the cancer diagnosis date?')
#         if cleaned_data.get('cancer_record') == 'Yes' and not cleaned_data.get('dx_cancer'):
#             raise forms.ValidationError('if cancer record is available on the OPD card, specify the cancer diagnosis?')
#         
#         #Validating that TB info is not given if patient has never been diagnosed with TB
#         if cleaned_data.get('tb') == 'No' and cleaned_data.get('tb_record') or cleaned_data.get('date_tb') or cleaned_data.get('dx_tb'):
#             raise forms.ValidationError('You are giving more TB related information yet have answered \'NO\',patient has never been diagnosed with TB to (Q95)')
#         #if patient ever had TB, is summary in OPD
#         if cleaned_data.get('tb') == 'Yes' and not cleaned_data.get('tb_record'):
#             raise forms.ValidationError('if patient has had TB, is there a record available on the OPD card?')
#         if cleaned_data.get('tb_record') == 'Yes' and not cleaned_data.get('date_tb'):
#             raise forms.ValidationError('if a TB record is available on the OPD card, give the TB diagnosis date')
#         if cleaned_data.get('tb_record') == 'Yes' and not cleaned_data.get('dx_tb'):
#             raise forms.ValidationError('if a TB record is available on the OPD card, what is the TB diagnosis type?')
#         

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
        
        #if other, specify
        if cleaned_data.get('often_medicalcare') == 'OTHER' and not cleaned_data.get('often_medicalcare_other'):
            raise forms.ValidationError('if other medical care is used, specify the kind of medical care received')
        if cleaned_data.get('whereaccess') == 'Other, specify' and not cleaned_data.get('whereaccess_other'):
            raise forms.ValidationError('if medical access is \'OTHER\', provide the type of medical access obtained')
        
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


# FutureHivTesting
class FutureHivTestingForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        
        #validating a need to specify the participant's preference 
        if cleaned_data.get('hiv_test_time') == 'Yes, specify' and not cleaned_data.get('hiv_test_time_other'):
            raise forms.ValidationError('If participant prefers a different test date/time than what is indicated, indicate the preference.')
        
        if cleaned_data.get('hiv_test_week') == 'Yes, specify' and not cleaned_data.get('hiv_test_week_other'):
            raise forms.ValidationError('If participant has preference for testing on a particular day of the week, indicate the preference.')
        
        if cleaned_data.get('hiv_test_year') == 'Yes, specify' and not cleaned_data.get('hiv_test_year_other'):
            raise forms.ValidationError('If participant prefers time of the year than the options given, indicate the preference.')
        
        cleaned_data = super(FutureHivTestingForm, self).clean()

        return cleaned_data

    class Meta:
        model = FutureHivTesting


class TodaysHivResultForm(BaseSubjectModelForm):
    
    def clean(self):
    
        cleaned_data = self.cleaned_data
    #validating when testing declined
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing (2)')
        
        cleaned_data = super(TodaysHivResultForm, self).clean()
        
        return cleaned_data
    
    class Meta:
        model = TodaysHivResult


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
