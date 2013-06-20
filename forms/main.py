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
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating if other community, you specify
        if cleaned_data['cattlepostlands'] == 'Other community' and not cleaned_data['cattlepostlands_other']:
            raise forms.ValidationError('If participant was staying in another community, specify the community')
        #if reason for staying away is OTHER, specify reason
        if cleaned_data['reasonaway'] == 'Other' and not cleaned_data['reasonaway_other']:
            raise forms.ValidationError('If participant was away from community for \'OTHER\' reason, provide/specify reason')
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        return cleaned_data

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
        #if no medical care, explain why not
        if cleaned_data['medical_care'] == 'No' and not cleaned_data['no_medical_care']:
            raise forms.ValidationError('If participant has not received any medical care, please give reason why not')
        #if never taken arv's give reason why
        if cleaned_data['evertakearv'] == 'No' and not cleaned_data['whynoarv']:
            raise forms.ValidationError('If participant has not taken any ARV\'s, give the main reason why not')
        #if partipant has taken arv's, give date when these were started
        if cleaned_data['evertakearv'] == 'Yes' and not cleaned_data['firstarv']:
            raise forms.ValidationError('If participant has taken ARV\'s, give the date when these were first started.')
        #if taking arv's have you missed any
        if cleaned_data['onarv'] == 'Yes' and not cleaned_data['adherence4day']:
            raise forms.ValidationError('If participant is taking ARV\'s, have they skipped/ missed taking any? Pleae indicate')
        #if you are not taking any arv's do not indicate that you have missed taking medication
        if cleaned_data['onarv'] == 'No' and cleaned_data['adherence4day']:
            raise forms.ValidationError('You do not have to indicate missed medication (70) because you are not taking any ARV\'s (68)')
        #if currently taking arv's, how well has participant been taking medication
        if cleaned_data['onarv'] == 'Yes' and cleaned_data['adherence4wk']:
            raise forms.ValidationError('If participant is currently taking ARV\'s, how well has he/she been taking the medication this past week?')

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
        #pregnancy and antenal registration
        if cleaned_data['currentpregnant'] == 'Yes' and not cleaned_data['ancreg']:
            raise forms.ValidationError('If participant currently pregnant, have they registered for antenatal care?')
        #if currently pregnant when was the last lnmp
        if cleaned_data['currentpregnant'] == 'Yes' and not cleaned_data['lnmp']:
            raise forms.ValidationError('If participant currently pregnant, when was the last known menstrual period?')
        #if mother has children, when was the last birth
        if cleaned_data['numberchildren'] > 0 and not cleaned_data['lastbirth']:
            raise forms.ValidationError('If the participant has given birth, when was the last (most recent) birth?')
        #if mother has children, did they ever go for anc
        if cleaned_data['numberchildren'] > 0 and not cleaned_data['anclastpregnancy']:
            raise forms.ValidationError('If the participant has children, during their last pregnancy, did they do for antenatal care?')
        #if mother has children, did they ever go for anc
        if cleaned_data['numberchildren'] > 0 and not cleaned_data['hivlastpregnancy']:
            raise forms.ValidationError('If the participant has children/ has given birth, did they ever test for HIV on their last pregnancy?')
        
        return cleaned_data

    class Meta:
        model = ReproductiveHealth


#MedicalDiagnoses
class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #Validating that heartattack info is not given if patient has never had a heartattach
        if cleaned_data['heartattack'] == 'No' and cleaned_data['heartattackrecord'] or cleaned_data['dateheartattack'] or cleaned_data['dxheartattack']:
            raise forms.ValidationError('You are giving more heartattack related information yet have answered \'NO\', to (Q86)')
        #if patient has had heart attack, is summary in OPD
        if cleaned_data['heartattack'] == 'Yes' and not cleaned_data['heartattackrecord']:
            raise forms.ValidationError('if patient has had a heart attack, is there a record available on the OPD card?')
        #if OPD record available, give date as on OPD
        if cleaned_data['heartattackrecord'] == 'Yes' and not cleaned_data['dateheartattack']:
            raise forms.ValidationError('If a record of the heart attack is available on the OPD card, give the date of diagnosis')
        #if OPD record available, give diagnosis as recorded on OPD
        if cleaned_data['heartattackrecord'] == 'Yes' and not cleaned_data['dxheartattack']:
            raise forms.ValidationError('If a record of the heart attack is available on the OPD card, provide the diagnosis detail (Q89).')
        
        #Validating that cancer info is not given if patient has never been diagnosed with cancer
        if cleaned_data['cancer'] == 'No' and cleaned_data['cancerrecord'] or cleaned_data['datecancer'] or cleaned_data['dxcancer']:
            raise forms.ValidationError('You are giving more cancer related information yet have answered \'NO\',patient has never been told he/she has cancer to (Q90)')
        #if patient has had cancer, is summary in OPD
        if cleaned_data['cancer'] == 'Yes' and not cleaned_data['cancerrecord']:
            raise forms.ValidationError('if patient has cancer, is there a cancer record available on the OPD card?')
        if cleaned_data['cancerrecord'] == 'Yes' and not cleaned_data['datecancer']:
            raise forms.ValidationError('if cancer record is available on the OPD card, what is the cancer diagnosis date?')
        if cleaned_data['cancerrecord'] == 'Yes' and not cleaned_data['dxcancer']:
            raise forms.ValidationError('if cancer record is available on the OPD card, specify the cancer diagnosis?')
        
        #Validating that TB info is not given if patient has never been diagnosed with TB
        if cleaned_data['tb'] == 'No' and cleaned_data['tbrecord'] or cleaned_data['datetb'] or cleaned_data['dxTB']:
            raise forms.ValidationError('You are giving more TB related information yet have answered \'NO\',patient has never been diagnosed with TB to (Q95)')
        #if patient ever had TB, is summary in OPD
        if cleaned_data['tb'] == 'Yes' and not cleaned_data['tbrecord']:
            raise forms.ValidationError('if patient has had TB, is there a record available on the OPD card?')
        if cleaned_data['tbrecord'] == 'Yes' and not cleaned_data['datetb']:
            raise forms.ValidationError('if a TB record is available on the OPD card, give the TB diagnosis date')
        if cleaned_data['tbrecord'] == 'Yes' and not cleaned_data['dxTB']:
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
        if cleaned_data['often_medicalcare'] == 'OTHER' and not cleaned_data['often_medicalcare_other']:
            raise forms.ValidationError('if other medical care is used, specify the kind of medical care received')
        if cleaned_data['whereaccess'] == 'Other, specify' and not cleaned_data['whereaccess_other']:
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
