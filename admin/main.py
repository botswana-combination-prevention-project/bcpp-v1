from django.contrib import admin
from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import (QualityOfLife, ResourceUtilization, OutpatientCare,
                                 HospitalAdmission, HivHealthCareCosts, CeaEnrolmentChecklist,
                                 CommunityEngagement, Education,
                                 HivMedicalCare, Circumcision, Circumcised,
                                 ReproductiveHealth, MedicalDiagnoses, HeartAttack,
                                 Cancer, Tubercolosis,
                                 SubstanceUse, Stigma, StigmaOpinion, PositiveParticipant, FutureHivTesting,
                                 HivResultDocumentation)
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import (QualityOfLifeForm, ResourceUtilizationForm, OutpatientCareForm,
                                HospitalAdmissionForm, HivHealthCareCostsForm,
                                CeaEnrolmentChecklistForm, CommunityEngagementForm,
                                EducationForm, HivMedicalCareForm,
                                CircumcisionForm, CircumcisedForm,
                                ReproductiveHealthForm, MedicalDiagnosesForm,
                                HeartAttackForm, CancerForm,
                                TubercolosisForm, SubstanceUseForm, StigmaForm,
                                StigmaOpinionForm, PositiveParticipantForm,
                                FutureHivTestingForm, HivResultDocumentationForm)


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


class EducationAdmin(SubjectVisitModelAdmin):

    form = EducationForm
    fields = (
        "subject_visit",
        'education',
        'working',
        'job_type',
        'reason_unemployed',
        'job_description',
        'monthly_income',)
    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }
    required_instructions = ("Read to Participant: Next, I will ask you some"
                              " questions about what education and work you"
                              " may have done or are currently doing.")
admin.site.register(Education, EducationAdmin)


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
        'prefer_hivtest': admin.VERTICAL,
        "hiv_test_time": admin.VERTICAL,
        "hiv_test_week": admin.VERTICAL,
        "hiv_test_year": admin.VERTICAL, }
    required_instructions = ("Note to Interviewer: If participant is known"
                              " to be HIV-infected (tested positive today or"
                              " previously), skip to the next section. "
                              "Read to Participant: The following questions are"
                              " about how you would like to have HIV testing in the future.")
admin.site.register(FutureHivTesting, FutureHivTestingAdmin)


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


class CircumcisionAdmin(SubjectVisitModelAdmin):

    form = CircumcisionForm
    fields = (
        "subject_visit",
        'circumcised',)
    radio_fields = {
         'circumcised': admin.VERTICAL, }
    required_instructions = ("Note to Interviewer: This section is to be completed"
                             " by male participants. SKIP for female participants."
                             "Read to Participant: Some men are circumcised. "
                             "Male circumcision is [enter site specific word] when"
                             " the foreskin of the man's penis has been cut off."
                             " I would like to ask you a few questions regarding"
                             " male circumcision. Here is a diagram to clarify what"
                             " a circumcised and uncircumcised man looks like.")
admin.site.register(Circumcision, CircumcisionAdmin)


class CircumcisedAdmin(SubjectVisitModelAdmin):

    form = CircumcisedForm
    supplemental_fields = SupplementalFields(
        ("circumcised",
        "health_benefits_smc",
        'where_circ', 
        'where_circ_other',
        'why_circ', 
        'why_circ_other'), p=0.18, group='MC')
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


class MedicalDiagnosesAdmin(SubjectVisitModelAdmin):

    form = MedicalDiagnosesForm
    fields = (
        "subject_visit",
       'diagnoses',
       'heart_attack_record',
       'cancer_record',
       'sti',
       'tb_record',)
    radio_fields = {
        "heart_attack_record": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "sti": admin.VERTICAL,
        "tb_record": admin.VERTICAL, }
    filter_horizontal = ('diagnoses',)
    required_instructions = ("Read to Participant: I am now going to ask you"
                             "some questions about major illnesses that you may"
                             "have had in the past 12 months. Sometimes people"
                             "call different sicknesses by different names."
                             "If you do not understand what I mean, please ask."
                             "Also, please remember that your answers will be"
                             "kept confidential.")
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
    radio_fields = {'dx_cancer': admin.VERTICAL, }
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


class SubstanceUseAdmin(SubjectVisitModelAdmin):

    form = SubstanceUseForm
    fields = (
        "subject_visit",
        'alcohol',
        'smoke',)
    radio_fields = {
        "alcohol": admin.VERTICAL,
        "smoke": admin.VERTICAL, }
    required_instructions = ("Read to Participant: I would like to now ask you"
                             "questions about drinking alcohol and smoking.")
admin.site.register(SubstanceUse, SubstanceUseAdmin)


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
    required_instructions = ("Interviewer Note: The following supplemental "
                             "questions are only asked for respondents NOT known"
                             " to have HIV. SKIP for respondents with known HIV infection."
                             "Read to Participant: Different people feel differently about"
                             " people living with HIV. I am going to ask you about issues"
                             " relevant to HIV and AIDS and also people living with HIV."
                             " Some of the questions during the interview will ask for your"
                             " opinion on how you think people living with HIV are treated."
                             "To start, when thinking about yourself, please tell me how "
                             "strongly you agree or disagree with the following statements.")
admin.site.register(Stigma, StigmaAdmin)


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
    required_instructions = ("Read to Participant: Using your own opinions and"
                             "thinking about this community, please tell me how"
                             "strongly you agree or disagree with the following"
                             "statements.")
admin.site.register(StigmaOpinion, StigmaOpinionAdmin)


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
    required_instructions = ("Interviewer Note: The following supplemental questions"
                             "are only asked for respondents with known HIV infection."
                             "SKIP for respondents without known HIV infection. "
                             "Read to Participant: You let us know earlier that you"
                             "are HIV positive. I would now like to ask you a few"
                             "questions about your experiences living with HIV."
                             "Please remember this interview and your responses"
                             "are private and confidential.In this section,"
                             "I'm going to read you statements"
                             " about how you may feel about yourself and your "
                             "HIV/AIDS infection. I would like you to tell me"
                             "if you strongly agree, agree, disagree or strongly"
                             " disagree with each statement?")
admin.site.register(PositiveParticipant, PositiveParticipantAdmin)


# class RespondentInlineAdmin(BaseTabularInline):
#     model = Respondent
# 
# 
# class HouseholdCompositionAdmin (SubjectVisitModelAdmin):
# 
#     form = HouseholdCompositionForm
#     inlines = [RespondentInlineAdmin, ]
#     fields = (
#         'housecode',
#         'physical_add',
#         'coordinates',
#         'contact',
#         'phone_number',)
#     radio_fields = {
#         "contact": admin.VERTICAL, }
# admin.site.register(HouseholdComposition, HouseholdCompositionAdmin)


class HivResultDocumentationAdmin (SubjectVisitModelAdmin):

    form = HivResultDocumentationForm
    fields = (
        'subject_visit',
        'result_date',
        'result_recorded',
        'result_doc_type',)
    radio_fields = {
        "result_recorded": admin.VERTICAL,
        'result_doc_type': admin.VERTICAL, }
admin.site.register(HivResultDocumentation, HivResultDocumentationAdmin)
