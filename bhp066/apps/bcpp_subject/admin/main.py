from django.contrib import admin
from ..models import (QualityOfLife, ResourceUtilization, OutpatientCare,
                      HospitalAdmission, HivHealthCareCosts,
                      HivMedicalCare, HeartAttack, Cancer, Sti,
                      Tubercolosis, SubstanceUse)
from ..forms import (QualityOfLifeForm, ResourceUtilizationForm, OutpatientCareForm,
                     HospitalAdmissionForm, HivHealthCareCostsForm,
                     HivMedicalCareForm,
                     HeartAttackForm, CancerForm, StiForm,
                     TubercolosisForm, SubstanceUseForm)
from .subject_visit_model_admin import SubjectVisitModelAdmin


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


class HeartAttackAdmin(SubjectVisitModelAdmin):

    form = HeartAttackForm
    fields = (
        "subject_visit",
       "date_heart_attack",
       'dx_heart_attack',
       'dx_heart_attack_other',)
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



class StiAdmin(SubjectVisitModelAdmin):

    form = StiForm
    fields = (
        "subject_visit",
       "sti_date",
       'sti_dx',
       'comments',)
    radio_fields = {'sti_dx': admin.VERTICAL, }
admin.site.register(Sti, StiAdmin)



class SubstanceUseAdmin(SubjectVisitModelAdmin):

    form = SubstanceUseForm
    fields = (
        "subject_visit",
        'alcohol',
        'smoke',)
    radio_fields = {
        "alcohol": admin.VERTICAL,
        "smoke": admin.VERTICAL, }
    instructions = [("Read to Participant: I would like to now ask you "
                             "questions about drinking alcohol and smoking.")]
admin.site.register(SubstanceUse, SubstanceUseAdmin)


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
