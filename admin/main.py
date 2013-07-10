from django.contrib import admin
from bhp_base_admin.admin import BaseTabularInline
from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import (QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, HivHealthCareCosts,
                                 LabourMarketWages, Grant, CeaEnrolmentChecklist, CsEnrolmentChecklist,
                                 CommunityEngagement, Education,
                                 HivTestReview, HivTested, HivUntested, MonthsRecentPartner, MonthsSecondPartner,
                                 MonthsThirdPartner, HivMedicalCare, Circumcision, Circumcised, Uncircumcised,
                                 ReproductiveHealth, MedicalDiagnoses, HeartAttack, Cancer, Tubercolosis, 
                                 SubstanceUse, Stigma, StigmaOpinion, PositiveParticipant,
                                 AccessToCare, HouseholdComposition, Respondent, FutureHivTesting, TodaysHivResult)
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import (QualityOfLifeForm, ResourceUtilizationForm, OutpatientCareForm, HospitalAdmissionForm,
                                HivHealthCareCostsForm, LabourMarketWagesForm, CeaEnrolmentChecklistForm,
                                CsEnrolmentChecklistForm, CommunityEngagementForm,
                                EducationForm, HivTestReviewForm, HivTestedForm, HivUntestedForm,
                                MonthsRecentPartnerForm, MonthsSecondPartnerForm, MonthsThirdPartnerForm,
                                HivMedicalCareForm, CircumcisionForm, CircumcisedForm, UncircumcisedForm,
                                ReproductiveHealthForm, MedicalDiagnosesForm, HeartAttackForm, CancerForm, 
                                TubercolosisForm, SubstanceUseForm, StigmaForm, StigmaOpinionForm, PositiveParticipantForm,
                                AccessToCareForm, HouseholdCompositionForm, FutureHivTestingForm, TodaysHivResultForm)


# QualityOfLife
class QualityOfLifeAdmin(SubjectVisitModelAdmin):

    form = QualityOfLifeForm
    fields = (
        "subject_visit",
        "mobility",
        "self_care",
        "activities",
        "pain",
        "anxiety",
        "health_today",
        )
    radio_fields = {
        "mobility": admin.VERTICAL,
        "self_care": admin.VERTICAL,
        "activities": admin.VERTICAL,
        "pain": admin.VERTICAL,
        "anxiety": admin.VERTICAL,
        }
admin.site.register(QualityOfLife, QualityOfLifeAdmin)


# ResourceUtilization
class ResourceUtilizationAdmin(SubjectVisitModelAdmin):

    form = ResourceUtilizationForm
    fields = (
        "subject_visit",
        "out_patient",
        "hospitalized",
        "money_spent",
        "medical_cover",
        )
    radio_fields = {
        "out_patient": admin.VERTICAL,
        "medical_cover": admin.VERTICAL,
        }
admin.site.register(ResourceUtilization, ResourceUtilizationAdmin)


class OutpatientCareAdmin(SubjectVisitModelAdmin):

    form = OutpatientCareForm
    fields = (
        "subject_visit",
        "govt_health_care",
        "dept_care",
        "prvt_care",
        "trad_care",
        "care_visits",
        "facility_visited",
        "specific_clinic",
        "care_reason",
        "care_reason_other",
        "outpatient_expense",
        "travel_time",
        "transport_expense",
        "cost_cover",
        "waiting_hours",
        )
    radio_fields = {
        "govt_health_care": admin.VERTICAL,
        "dept_care": admin.VERTICAL,
        "prvt_care": admin.VERTICAL,
        "trad_care": admin.VERTICAL,
        "facility_visited": admin.VERTICAL,
        "care_reason": admin.VERTICAL,
        "travel_time": admin.VERTICAL,
        "cost_cover": admin.VERTICAL,
        "waiting_hours": admin.VERTICAL,
        }
admin.site.register(OutpatientCare, OutpatientCareAdmin)


# HospitalAdmission
class HospitalAdmissionAdmin(SubjectVisitModelAdmin):

    form = HospitalAdmissionForm
    fields = (
        "subject_visit",
        "admission_nights",
        "reason_hospitalized",
        "facility_hospitalized",
        "nights_hospitalized",
        "healthcare_expense",
        "travel_hours",
        "total_expenses",
        "hospitalization_costs",
        )
    radio_fields = {
        "reason_hospitalized": admin.VERTICAL,
        "travel_hours": admin.VERTICAL,
        "hospitalization_costs": admin.VERTICAL,
        }
admin.site.register(HospitalAdmission, HospitalAdmissionAdmin)


# HivHealthCareCosts
class HivHealthCareCostsAdmin(SubjectVisitModelAdmin):

    form = HivHealthCareCostsForm
    fields = (
        "subject_visit",
        "hiv_medical_care",
        "reason_no_care",
        "place_care_received",
        "care_regularity",
        "doctor_visits",
        )
    radio_fields = {
        "hiv_medical_care": admin.VERTICAL,
        "reason_no_care": admin.VERTICAL,
        "place_care_received": admin.VERTICAL,
        "care_regularity": admin.VERTICAL,
        "doctor_visits": admin.VERTICAL,
        }
admin.site.register(HivHealthCareCosts, HivHealthCareCostsAdmin)


# Grant
class GrantInlineAdmin(BaseTabularInline):
    model = Grant


# LabourMarketWages
class LabourMarketWagesAdmin(SubjectVisitModelAdmin):

    form = LabourMarketWagesForm
    inlines = [GrantInlineAdmin, ]
    fields = (
        "subject_visit",
        "employed",
        "occupation",
        "occupation_other",
        "job_description_change",
        "days_worked",
        "monthly_income",
        "salary_payment",
        "household_income",
        "other_occupation",
        "other_occupation_other",
        "govt_grant",
        "nights_out",
        "weeks_out",
        "days_not_worked",
        "days_inactivite",
        )
    radio_fields = {
        "employed": admin.VERTICAL,
        "occupation": admin.VERTICAL,
        "monthly_income": admin.VERTICAL,
        "salary_payment": admin.VERTICAL,
        "household_income": admin.VERTICAL,
        "other_occupation": admin.VERTICAL,
        "govt_grant": admin.VERTICAL,
        "weeks_out": admin.VERTICAL,
        }
admin.site.register(LabourMarketWages, LabourMarketWagesAdmin)


# CeaEnrolmentChecklist
class CeaEnrolmentChecklistAdmin(RegisteredSubjectModelAdmin):

    form = CeaEnrolmentChecklistForm
    fields = (
        "registered_subject",
#         "registration_datetime",
        "mental_capacity",
        "incarceration",
        "citizen",
        "community_resident",
        "enrolment_reason",
        "cd4_date",
        "cd4_count",
        "opportunistic_illness",
        "diagnosis_date",
        "date_signed",)
    radio_fields = {
        "mental_capacity": admin.VERTICAL,
        "incarceration": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "community_resident": admin.VERTICAL,
        "enrolment_reason": admin.VERTICAL,
        "opportunistic_illness": admin.VERTICAL, }
admin.site.register(CeaEnrolmentChecklist, CeaEnrolmentChecklistAdmin)


# CsEnrolmentChecklist
class CsEnrolmentChecklistAdmin(RegisteredSubjectModelAdmin):

    form = CsEnrolmentChecklistForm
    fields = (
        "registered_subject",
        "registration_datetime",
        "census_number",
        "mental_capacity",
        "incarceration",
        "citizen",
        "community_resident",
        "date_minor_signed",
        "date_guardian_signed",
        "date_consent_signed",)
    radio_fields = {
        "mental_capacity": admin.VERTICAL,
        "incarceration": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "community_resident": admin.VERTICAL, }
admin.site.register(CsEnrolmentChecklist, CsEnrolmentChecklistAdmin)


# CommunityEngagement
class CommunityEngagementAdmin(SubjectVisitModelAdmin):

    form = CommunityEngagementForm
    fields = (
        "subject_visit",
        'community_engagement',
        'vote_engagement',
        'problems_engagement',
        'problems_engagement_other',
        'solve_engagement',)
    radio_fields = {
        "community_engagement": admin.VERTICAL,
        "vote_engagement": admin.VERTICAL,
        "solve_engagement": admin.VERTICAL, }
    filter_horizontal = ('problems_engagement',)
admin.site.register(CommunityEngagement, CommunityEngagementAdmin)


# Education
class EducationAdmin(SubjectVisitModelAdmin):

    form = EducationForm
    fields = (
        "subject_visit",
        'education',
        'employment',
        'money_forwork',
        'seeking_work',)
    radio_fields = {
        "education": admin.VERTICAL,
        "employment": admin.VERTICAL,
        "money_forwork": admin.VERTICAL,
        "seeking_work": admin.VERTICAL, }
admin.site.register(Education, EducationAdmin)


# HivTestReview
class HivTestReviewAdmin(SubjectVisitModelAdmin):

    form = HivTestReviewForm
    fields = (
        "subject_visit",
        'hiv_test_date',
        'recorded_hiv_result')
    radio_fields = {
        "recorded_hiv_result": admin.VERTICAL, }
admin.site.register(HivTestReview, HivTestReviewAdmin)


# HivTested
class HivTestedAdmin(SubjectVisitModelAdmin):

    form = HivTestedForm
    fields = (
        "subject_visit",
        'num_hiv_tests',
        'where_hiv_test',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "where_hiv_test":admin.VERTICAL,
        "why_hiv_test":admin.VERTICAL,
        "hiv_pills":admin.VERTICAL,
        "arvs_hiv_test":admin.VERTICAL,}
admin.site.register(HivTested, HivTestedAdmin)


#HivUntested 
class HivUntestedAdmin(SubjectVisitModelAdmin):
 
    form = HivUntestedForm
    fields = (
        "subject_visit",
        'why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "why_no_hiv_test":admin.VERTICAL,
        "hiv_pills":admin.VERTICAL,
        "arvs_hiv_test":admin.VERTICAL,}
admin.site.register(HivUntested, HivUntestedAdmin)


# # HivTestingSupplemental 
# class HivTestingSupplementalAdmin(SubjectVisitModelAdmin):
#  
#     form = HivTestingSupplementalForm
#     fields = (
#         "subject_visit",
#         'numhivtests',
#         'wherehivtest',
#         'whyhivtest',
#         'whynohivtest',
#         'hiv_pills',
#         'arvshivtest',)
#     radio_fields = {
#         "wherehivtest":admin.VERTICAL,
#         "whyhivtest":admin.VERTICAL,
#         "whynohivtest":admin.VERTICAL,
#         "hiv_pills":admin.VERTICAL,
#         "arvshivtest":admin.VERTICAL}
# admin.site.register(HivTestingSupplemental, HivTestingSupplementalAdmin)


# FutureHivTesting 
class FutureHivTestingAdmin(SubjectVisitModelAdmin):
 
    form = FutureHivTestingForm
    fields = (
        "subject_visit",
        'prefer_hivtest',
        'hiv_test_time',
        'hiv_test_time_other',
        'hiv_test_week',
        'hiv_test_week_other',
        'hiv_test_year',
        'hiv_test_year_other')
    radio_fields = {
        'prefer_hivtest':admin.VERTICAL,
        "hiv_test_time":admin.VERTICAL,
        "hiv_test_week":admin.VERTICAL,
        "hiv_test_year":admin.VERTICAL,}
admin.site.register(FutureHivTesting, FutureHivTestingAdmin)


# MonthsRecentPartner
class MonthsRecentPartnerAdmin(SubjectVisitModelAdmin):

    form = MonthsRecentPartnerForm
    supplemental_fields = SupplementalFields(
        ('first_partner_hiv',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp'), p=0.1, group='HT')
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
admin.site.register(MonthsRecentPartner, MonthsRecentPartnerAdmin)


# MonthsSecondPartner
class MonthsSecondPartnerAdmin(SubjectVisitModelAdmin):

    form = MonthsSecondPartnerForm
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
admin.site.register(MonthsSecondPartner, MonthsSecondPartnerAdmin)


# MonthsThirdPartner
class MonthsThirdPartnerAdmin(SubjectVisitModelAdmin):

    form = MonthsThirdPartnerForm
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
admin.site.register(MonthsThirdPartner, MonthsThirdPartnerAdmin)


# HivMedicalCare
class HivMedicalCareAdmin(SubjectVisitModelAdmin):

    form = HivMedicalCareForm
    fields = (
        "subject_visit",
        "first_hiv_care_pos",
        "last_hiv_care_pos",
        'lowest_cd4',)
    radio_fields = {
        "lowest_cd4": admin.VERTICAL}
admin.site.register(HivMedicalCare, HivMedicalCareAdmin)


# Circumcision
class CircumcisionAdmin(SubjectVisitModelAdmin):

    form = CircumcisionForm
    fields = (
        "subject_visit",
        'circumcised',)
    radio_fields = {
         'circumcised': admin.VERTICAL, }
admin.site.register(Circumcision, CircumcisionAdmin)


# Circumcised
class CircumcisedAdmin(SubjectVisitModelAdmin):

    form = CircumcisedForm
    fields = (
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'when_circ',
        'where_circ',
        'where_circ_other',
        'why_circ',
        'why_circ_other',)
    radio_fields = {
        "circumcised": admin.VERTICAL,
        "where_circ": admin.VERTICAL,
        "why_circ": admin.VERTICAL, }
    filter_horizontal = ("health_benefits_smc",)
admin.site.register(Circumcised, CircumcisedAdmin)


# Uncircumcised
class UncircumcisedAdmin(SubjectVisitModelAdmin):

    form = UncircumcisedForm
    fields = [
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'reason_circ',
        'future_circ',
        'circumcision_day',
        'circumcision_day_other',
        'circumcision_week',
        'circumcision_week_other',
        'circumcision_year',
        'circumcision_year_other',
        'future_reasons_smc',
        'service_facilities',
        'aware_free',
    ]
    radio_fields = {
        "circumcised": admin.VERTICAL,
        "reason_circ": admin.VERTICAL,
        "future_circ": admin.VERTICAL,
        "circumcision_day": admin.VERTICAL,
        "circumcision_week": admin.VERTICAL,
        "circumcision_year": admin.VERTICAL,
        "future_reasons_smc": admin.VERTICAL,
        "service_facilities": admin.VERTICAL,
        "aware_free": admin.VERTICAL}
    filter_horizontal = ("health_benefits_smc",)
admin.site.register(Uncircumcised, UncircumcisedAdmin)


class ReproductiveHealthAdmin(SubjectVisitModelAdmin):
    
    form = ReproductiveHealthForm
    fields = (
        "subject_visit",
        "number_children",
        "menopause",
        )
    radio_field = {
        "menopause": admin.VERTICAL,}
admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)


# MedicalDiagnoses
class MedicalDiagnosesAdmin(SubjectVisitModelAdmin):

    form = MedicalDiagnosesForm
    fields = (
        "subject_visit",
       'diagnoses',
#        'heart_attack',
       'heart_attack_record',
#        'cancer',
       'cancer_record',
       'sti',
#        'tb',
       'tb_record',)
    radio_fields = {
#         "heart_attack": admin.VERTICAL,
        "heart_attack_record": admin.VERTICAL,
#         "cancer": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "sti": admin.VERTICAL,
#         "tb": admin.VERTICAL,
        "tb_record": admin.VERTICAL,}
admin.site.register(MedicalDiagnoses, MedicalDiagnosesAdmin)


class HeartAttackAdmin(SubjectVisitModelAdmin):

    form = HeartAttackForm
    fields = (
        "subject_visit",
       "date_heart_attack",
       'dx_heart_attack',)
    filter_horizontal = ('dx_heart_attack',)
admin.site.register(HeartAttack, HeartAttackAdmin)


class CancerAdmin(SubjectVisitModelAdmin):

    form = CancerForm
    fields = (
        "subject_visit",
       "date_cancer",
       'dx_cancer',)
    radio_fields = {'dx_cancer': admin.VERTICAL,}
admin.site.register(Cancer, CancerAdmin)


class TubercolosisAdmin(SubjectVisitModelAdmin):

    form = TubercolosisForm
    fields = (
        "subject_visit",
       "date_tb",
       'dx_tb',)
    radio_fields = {
        "dx_tb": admin.VERTICAL, }
admin.site.register(Tubercolosis, TubercolosisAdmin)


# SubstanceUse
class SubstanceUseAdmin(SubjectVisitModelAdmin):

    form = SubstanceUseForm
    fields = (
        "subject_visit",
        'alcohol',
        'smoke',)
    radio_fields = {
        "alcohol": admin.VERTICAL,
        "smoke": admin.VERTICAL, }
admin.site.register(SubstanceUse, SubstanceUseAdmin)


# Stigma
class StigmaAdmin(SubjectVisitModelAdmin):

    form = StigmaForm
    fields = (
        "subject_visit",
        'anticipate_stigma',
        'enacted_shame_stigma',
        'saliva_stigma',
        'teacher_stigma',
        'children_stigma',)
    radio_fields = {
        "anticipate_stigma": admin.VERTICAL,
        "enacted_shame_stigma": admin.VERTICAL,
        "saliva_stigma": admin.VERTICAL,
        "teacher_stigma": admin.VERTICAL,
        "children_stigma": admin.VERTICAL, }
admin.site.register(Stigma, StigmaAdmin)


# StigmaOpinion
class StigmaOpinionAdmin(SubjectVisitModelAdmin):

    form = StigmaOpinionForm
    fields = (
        "subject_visit",
        'test_community_stigma',
        'gossip_community_stigma',
        'respect_community_stigma',
        'enacted_verbal_stigma',
        'enacted_phyical_stigma',
        'enacted_family_stigma',
        'fear_stigma',)
    radio_fields = {
        "test_community_stigma": admin.VERTICAL,
        "gossip_community_stigma": admin.VERTICAL,
        "respect_community_stigma": admin.VERTICAL,
        "enacted_verbal_stigma": admin.VERTICAL,
        "enacted_phyical_stigma": admin.VERTICAL,
        "enacted_family_stigma": admin.VERTICAL,
        "fear_stigma": admin.VERTICAL, }
admin.site.register(StigmaOpinion, StigmaOpinionAdmin)


# PositiveParticipant
class PositiveParticipantAdmin(SubjectVisitModelAdmin):

    form = PositiveParticipantForm
    fields = (
        "subject_visit",
        'internalize_stigma',
        'internalized_stigma',
        'friend_stigma',
        'family_stigma',
        'enacted_talk_stigma',
        'enacted_respect_stigma',
        'enacted_jobs_tigma',)
    radio_fields = {
        "internalize_stigma": admin.VERTICAL,
        "internalized_stigma": admin.VERTICAL,
        "friend_stigma": admin.VERTICAL,
        "family_stigma": admin.VERTICAL,
        "enacted_talk_stigma": admin.VERTICAL,
        "enacted_respect_stigma": admin.VERTICAL,
        "enacted_jobs_tigma": admin.VERTICAL, }
admin.site.register(PositiveParticipant, PositiveParticipantAdmin)


# AccessToCare
class AccessToCareAdmin(SubjectVisitModelAdmin):

    form = AccessToCareForm

    fields = (
        "subject_visit",
        "report_datetime",
        "access_care",
        "access_care_other",
        "medical_care_access",
        "medical_care_access_other",
        "overall_access",
        "emergency_access",
        "expensive_access",
        "convenient_access",
        "whenever_access"
    )

    radio_fields = {
        "access_care": admin.VERTICAL,
        "overall_access": admin.VERTICAL,
        "emergency_access": admin.VERTICAL,
        "expensive_access": admin.VERTICAL,
        "convenient_access": admin.VERTICAL,
        "whenever_access": admin.VERTICAL
    }

    filter_horizontal = (
        "medical_care_access",
    )
admin.site.register(AccessToCare, AccessToCareAdmin)


class RespondentInlineAdmin(BaseTabularInline):
    model = Respondent


class HouseholdCompositionAdmin (SubjectVisitModelAdmin):

    form = HouseholdCompositionForm
    inlines = [RespondentInlineAdmin, ]
    fields = (
        'housecode',
        'physical_add',
        'coordinates',
        'contact',
        'phone_number',)
    radio_fields = {
        "contact":admin.VERTICAL,}
admin.site.register(HouseholdComposition, HouseholdCompositionAdmin)


class TodaysHivResultAdmin (SubjectVisitModelAdmin):

    form = TodaysHivResultForm
    fields = (
        'subject_visit',
        'hiv_result')
    radio_fields = {
        "hiv_result":admin.VERTICAL,}
admin.site.register(TodaysHivResult, TodaysHivResultAdmin)
