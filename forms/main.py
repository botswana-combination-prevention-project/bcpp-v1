from django import forms
from datetime import datetime
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import (SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner, 
                                 QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, 
                                 HivHealthCareCosts, LabourMarketWages, Grant, BaselineHouseholdSurvey, 
                                 CeaEnrolmentChecklist, CsEnrolmentChecklist, ResidencyMobility, 
                                 Demographics, CommunityEngagement, Education, HivTestingHistory, 
                                 HivTestReview, HivTested, HivUntested, FutureHivTesting, SexualBehaviour, 
                                 MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner, 
                                 HivCareAdherence, HivMedicalCare, Circumcision, Circumcised, Uncircumcised, 
                                 ReproductiveHealth, MedicalDiagnoses, SubstanceUse, Stigma, StigmaOpinion, 
                                 PositiveParticipant, AccessToCare, HouseholdComposition, 
                                 Respondent)


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
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating if other, specify
        if cleaned_data.get('flooring_type') == 'OTHER' and not cleaned_data.get('flooring_type_other'):
            raise forms.ValidationError('If participant has a different flooring type from what is on the list, provide the flooring type')
        if cleaned_data.get('water_source') == 'OTHER' and not cleaned_data.get('water_source_other'):
            raise forms.ValidationError('If participant uses a different water source, specify it')
        if cleaned_data.get('energy_source') == 'OTHER' and not cleaned_data.get('energy_source_other'):
            raise forms.ValidationError('If a different energy source is used, specify it')
        cleaned_data = super(BaselineHouseholdSurveyForm, self).clean()
        return cleaned_data

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
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating if other community, you specify
        if cleaned_data.get('cattle_postlands') == 'Other community' and not cleaned_data.get('cattle_postlands_other'):
            raise forms.ValidationError('If participant was staying in another community, specify the community')
        #if reason for staying away is OTHER, specify reason
        if cleaned_data.get('reason_away') == 'Other' and not cleaned_data.get('reason_away_other'):
            raise forms.ValidationError('If participant was away from community for \'OTHER\' reason, provide/specify reason')
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        return cleaned_data

    class Meta:
        model = ResidencyMobility


#Demographics
class DemographicsForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating religion affiliation
        if cleaned_data.get('religion') == 'Christian' and not cleaned_data.get('religion_other'):
            raise forms.ValidationError('If participant is a Christian, specify denomination.')
        #validating ethnicity
        if cleaned_data.get('ethnic') == 'Tswana' and not cleaned_data.get('other'):
            raise forms.ValidationError('If participant is Tswana, specify the ethnic group.')
        #validating Other
        if cleaned_data.get('ethnic') == 'Other' and not cleaned_data.get('other'):
            raise forms.ValidationError('If participant ethnic group not given in list-of-options, specify the ethnic group.')
        #validating marital status
        if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('num_wives'):
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
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
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

#SexualBehaviour
class SexualBehaviourForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #if respondent has had sex, answer all following questions on form
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('last_year_partners'):
            raise forms.ValidationError('If participant has had sex, how many people has he/she had sex with')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('more_sex'):
            raise forms.ValidationError('If participant has had sex, we need to know if this person lives outside community')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('first_sex'):
            raise forms.ValidationError('If participant has had sex, how old was he/she when he/she first had sex')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('condom'):
            raise forms.ValidationError('If participant has had sex, was a condom used the last time he/she had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('alcohol_sex'):
            raise forms.ValidationError('If participant has had sex, did he/she or partner have alcohol?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('last_sex'):
            raise forms.ValidationError('If participant has had sex, when was the last time he/she had sex?')
        if cleaned_data.get('last_sex') == 'Days' and not cleaned_data.get('last_sex_calc'):
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of days')
        if cleaned_data.get('last_sex') == 'Months' and not cleaned_data.get('last_sex_calc'):
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of months')
        if cleaned_data.get('last_sex') == 'Years' and not cleaned_data.get('last_sex_calc'):
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



#HivCareAdherence
class HivCareAdherenceForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #if no medical care, explain why not
        if cleaned_data.get('medical_care') == 'No' and not cleaned_data.get('no_medical_care'):
            raise forms.ValidationError('If participant has not received any medical care, please give reason why not')
        #if never taken arv's give reason why
        if cleaned_data.get('ever_recommended_arv') == 'No' and not cleaned_data.get('why_no_arv'):
            raise forms.ValidationError('If participant has not taken any ARV\'s, give the main reason why not')
        if cleaned_data.get('why_no_arv') == 'Other' and not cleaned_data.get('why_no_arv_other'):
            raise forms.ValidationError('If participant NO ARV\'s is \'OTHER\', specify reason why not started ARV\'s?')
        #if partipant has taken arv's, give date when these were started
        if cleaned_data.get('ever_recommended_arv') == 'Yes' and not cleaned_data.get('first_arv'):
            raise forms.ValidationError('If participant has taken ARV\'s, give the date when these were first started.')
        #if taking arv's have you missed any
        if cleaned_data.get('on_arv') == 'Yes' and not cleaned_data.get('adherence_4_day'):
            raise forms.ValidationError('If participant is taking ARV\'s, have they skipped/ missed taking any? Pleae indicate')
        #if you are not taking any arv's do not indicate that you have missed taking medication
        if cleaned_data.get('on_arv') == 'No' and cleaned_data.get('adherence_4_day'):
            raise forms.ValidationError('You do not have to indicate missed medication (70) because you are not taking any ARV\'s (68)')
        #if currently taking arv's, how well has participant been taking medication
        if cleaned_data.get('on_arv') == 'Yes' and cleaned_data.get('adherence_4_wk'):
            raise forms.ValidationError('If participant is currently taking ARV\'s, how well has he/she been taking the medication this past week?')
        if cleaned_data.get('arv_stop') == 'Other' and not cleaned_data.get('arv_stop_other'):
            raise forms.ValidationError('If participant reason for stopping ARV\'s is \'OTHER\', specify reason why stopped taking ARV\'s?')

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


#ReproductiveHealth
class ReproductiveHealthForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #pregnancy and antenal registration
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('anc_reg'):
            raise forms.ValidationError('If participant currently pregnant, have they registered for antenatal care?')
        #if currently pregnant when was the last lnmp
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('lnmp'):
            raise forms.ValidationError('If participant currently pregnant, when was the last known menstrual period?')
        #if mother has children, when was the last birth
        if cleaned_data.get('number_children') > 0 and not cleaned_data.get('last_birth'):
            raise forms.ValidationError('If the participant has given birth, when was the last (most recent) birth?')
        #if mother has children, did they ever go for anc
        if cleaned_data.get('number_children') > 0 and not cleaned_data.get('anc_last_pregnancy'):
            raise forms.ValidationError('If the participant has children, during their last pregnancy, did they do for antenatal care?')
        #if mother has children, did they ever go for anc
        if cleaned_data.get('number_children') > 0 and not cleaned_data.get('hiv_last_pregnancy'):
            raise forms.ValidationError('If the participant has children/ has given birth, did they ever test for HIV on their last pregnancy?')
        
        return cleaned_data

    class Meta:
        model = ReproductiveHealth


#MedicalDiagnoses
class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #Validating that heartattack info is not given if patient has never had a heartattach
        if cleaned_data.get('heart_attack') == 'No' and cleaned_data.get('heart_attack_record') or cleaned_data.get('date_heart_attack') or cleaned_data.get('dx_heart_attack'):
            raise forms.ValidationError('You are giving more heart_attack related information yet have answered \'NO\', to (Q86)')
        #if patient has had heart attack, is summary in OPD
        if cleaned_data.get('heart_attack') == 'Yes' and not cleaned_data.get('heart_attack_record'):
            raise forms.ValidationError('if patient has had a heart attack, is there a record available on the OPD card?')
        #if OPD record available, give date as on OPD
        if cleaned_data.get('heart_attack_record') == 'Yes' and not cleaned_data.get('date_heart_attack'):
            raise forms.ValidationError('If a record of the heart attack is available on the OPD card, give the date of diagnosis')
        #if OPD record available, give diagnosis as recorded on OPD
        if cleaned_data.get('heart_attack_record') == 'Yes' and not cleaned_data.get('dx_heart_attack'):
            raise forms.ValidationError('If a record of the heart attack is available on the OPD card, provide the diagnosis detail (Q89).')
        
        #Validating that cancer info is not given if patient has never been diagnosed with cancer
        if cleaned_data.get('cancer') == 'No' and cleaned_data.get('cancer_record') or cleaned_data.get('date_cancer') or cleaned_data.get('dx_cancer'):
            raise forms.ValidationError('You are giving more cancer related information yet have answered \'NO\',patient has never been told he/she has cancer to (Q90)')
        #if patient has had cancer, is summary in OPD
        if cleaned_data.get('cancer') == 'Yes' and not cleaned_data.get('cancer_record'):
            raise forms.ValidationError('if patient has cancer, is there a cancer record available on the OPD card?')
        if cleaned_data.get('cancer_record') == 'Yes' and not cleaned_data.get('date_cancer'):
            raise forms.ValidationError('if cancer record is available on the OPD card, what is the cancer diagnosis date?')
        if cleaned_data.get('cancer_record') == 'Yes' and not cleaned_data.get('dx_cancer'):
            raise forms.ValidationError('if cancer record is available on the OPD card, specify the cancer diagnosis?')
        
        #Validating that TB info is not given if patient has never been diagnosed with TB
        if cleaned_data.get('tb') == 'No' and cleaned_data.get('tb_record') or cleaned_data.get('date_tb') or cleaned_data.get('dx_tb'):
            raise forms.ValidationError('You are giving more TB related information yet have answered \'NO\',patient has never been diagnosed with TB to (Q95)')
        #if patient ever had TB, is summary in OPD
        if cleaned_data.get('tb') == 'Yes' and not cleaned_data.get('tb_record'):
            raise forms.ValidationError('if patient has had TB, is there a record available on the OPD card?')
        if cleaned_data.get('tb_record') == 'Yes' and not cleaned_data.get('date_tb'):
            raise forms.ValidationError('if a TB record is available on the OPD card, give the TB diagnosis date')
        if cleaned_data.get('tb_record') == 'Yes' and not cleaned_data.get('dx_tb'):
            raise forms.ValidationError('if a TB record is available on the OPD card, what is the TB diagnosis type?')
        

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
