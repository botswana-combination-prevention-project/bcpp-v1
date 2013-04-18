from django.contrib import admin
from bhp_base_model.classes import BaseTabularInline
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner, QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, HivHealthCareCosts, LabourMarketWages, Grant, BaselineHouseholdSurvey, CeaEnrolmentChecklist, CsEnrolmentChecklist
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import SubjectLocatorForm, SubjectDeathForm, RecentPartnerForm, SecondPartnerForm, ThirdPartnerForm, QualityOfLifeForm, ResourceUtilizationForm, OutpatientCareForm, HospitalAdmissionForm, HivHealthCareCostsForm, LabourMarketWagesForm, BaselineHouseholdSurveyForm, CeaEnrolmentChecklistForm, CsEnrolmentChecklistForm


class SubjectLocatorAdmin(SubjectVisitModelAdmin):

    form = SubjectLocatorForm
    fields = (
        'subject_visit',
        'date_signed',
        'mail_address',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'alt_contact_cell_number',
        'contact_phone',
        'has_alt_contact',
        'alt_contact_name',
        'alt_contact_rel',
        'alt_contact_cell',
        'other_alt_contact_cell',
        'alt_contact_tel',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',)
    radio_fields = {
        "home_visit_permission": admin.VERTICAL,
        "may_follow_up": admin.VERTICAL,
        "has_alt_contact": admin.VERTICAL,
        "may_call_work": admin.VERTICAL,
        "may_contact_someone": admin.VERTICAL, }
admin.site.register(SubjectLocator, SubjectLocatorAdmin)


# SubjectDeath
class SubjectDeathAdmin(RegisteredSubjectModelAdmin):

    form = SubjectDeathForm
    fields = (
        "registered_subject",
        "sufficient_records",
        "document_hiv",
        "document_community",
        "document_community_other",
        "death_year",
        "death_cause_info",
        "decendent_death_age",
        "hospital_death",
        "decedent_haart",
        "decedent_haart_start",
        "decedent_hospitalized",
        "days_decedent_hospitalized",
        "hospital_visits",
        "doctor_evaluation",
        "comment")
    radio_fields = {
        "sufficient_records": admin.VERTICAL,
        "document_hiv": admin.VERTICAL,
        "document_community": admin.VERTICAL,
        "death_cause_info": admin.VERTICAL,
        "hospital_death": admin.VERTICAL,
        "decedent_haart": admin.VERTICAL,
        "decedent_hospitalized": admin.VERTICAL,
        }
admin.site.register(SubjectDeath, SubjectDeathAdmin)


# RecentPartner
class RecentPartnerAdmin(SubjectVisitModelAdmin):

    form = RecentPartnerForm
    fields = (
        "subject_visit",
        "rel_type",
        "rel_type_other",
        "partner_residency",
        "partner_age",
        "partner_gender",
        "last_sex_contact",
        "last_sex_contact_other",
        "first_sex_contact",
        "first_sex_contact_other",
        "regular_sex",
        "having_sex",
        "having_sex_reg",
        "alcohol_before_sex",
        "partner_status",
        "partner_arv",
        "status_disclosure",
        "multiple_partners",
        "intercourse_type")
    radio_fields = {
        "rel_type": admin.VERTICAL,
        "partner_residency": admin.VERTICAL,
        "partner_gender": admin.VERTICAL,
        "last_sex_contact": admin.VERTICAL,
        "first_sex_contact": admin.VERTICAL,
        "having_sex": admin.VERTICAL,
        "having_sex_reg": admin.VERTICAL,
        "alcohol_before_sex": admin.VERTICAL,
        "partner_status": admin.VERTICAL,
        "partner_arv": admin.VERTICAL,
        "status_disclosure": admin.VERTICAL,
        "multiple_partners": admin.VERTICAL,
        "intercourse_type": admin.VERTICAL,
        }
admin.site.register(RecentPartner, RecentPartnerAdmin)


# SecondPartner
class SecondPartnerAdmin(SubjectVisitModelAdmin):

    form = SecondPartnerForm
    fields = (
        "subject_visit",
        "rel_type",
        "rel_type_other",
        "partner_residency",
        "partner_age",
        "partner_gender",
        "last_sex_contact",
        "last_sex_contact_other",
        "first_sex_contact",
        "first_sex_contact_other",
        "regular_sex",
        "having_sex",
        "having_sex_reg",
        "alcohol_before_sex",
        "partner_status",
        "partner_arv",
        "status_disclosure",
        "multiple_partners",
        "intercourse_type")
    radio_fields = {
        "rel_type": admin.VERTICAL,
        "partner_residency": admin.VERTICAL,
        "partner_gender": admin.VERTICAL,
        "last_sex_contact": admin.VERTICAL,
        "first_sex_contact": admin.VERTICAL,
        "having_sex": admin.VERTICAL,
        "having_sex_reg": admin.VERTICAL,
        "alcohol_before_sex": admin.VERTICAL,
        "partner_status": admin.VERTICAL,
        "partner_arv": admin.VERTICAL,
        "status_disclosure": admin.VERTICAL,
        "multiple_partners": admin.VERTICAL,
        "intercourse_type": admin.VERTICAL,
        }
admin.site.register(SecondPartner, SecondPartnerAdmin)


# ThirdPartner
class ThirdPartnerAdmin(SubjectVisitModelAdmin):

    form = ThirdPartnerForm
    fields = (
        "subject_visit",
        "rel_type",
        "rel_type_other",
        "partner_residency",
        "partner_age",
        "partner_gender",
        "last_sex_contact",
        "last_sex_contact_other",
        "first_sex_contact",
        "first_sex_contact_other",
        "regular_sex",
        "having_sex",
        "having_sex_reg",
        "alcohol_before_sex",
        "partner_status",
        "partner_arv",
        "status_disclosure",
        "multiple_partners",
        "intercourse_type")
    radio_fields = {
        "rel_type": admin.VERTICAL,
        "partner_residency": admin.VERTICAL,
        "partner_gender": admin.VERTICAL,
        "last_sex_contact": admin.VERTICAL,
        "first_sex_contact": admin.VERTICAL,
        "having_sex": admin.VERTICAL,
        "having_sex_reg": admin.VERTICAL,
        "alcohol_before_sex": admin.VERTICAL,
        "partner_status": admin.VERTICAL,
        "partner_arv": admin.VERTICAL,
        "status_disclosure": admin.VERTICAL,
        "multiple_partners": admin.VERTICAL,
        "intercourse_type": admin.VERTICAL,
        }
admin.site.register(ThirdPartner, ThirdPartnerAdmin)


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


# OutpatientCare
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


#HospitalAdmission
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


# BaselineHouseholdSurvey
class BaselineHouseholdSurveyAdmin(SubjectVisitModelAdmin):

    form = BaselineHouseholdSurveyForm
    fields = (
        "subject_visit",
        "flooring_type",
        "flooring_type_other",
        "living_rooms",
        "water_source",
        "water_source_other",
        "energy_source",
        "toilet_facility",
        "electrical_appliances",
        "transport_mode",
        "goats_owned",
        "sheep_owned",
        "cattle_owned",
        "smaller_meals",
        )
    radio_fields = {
        "flooring_type": admin.VERTICAL,
        "water_source": admin.VERTICAL,
        "energy_source": admin.VERTICAL,
        "toilet_facility": admin.VERTICAL,
        "smaller_meals": admin.VERTICAL,
        }
    filter_horizontal = (
        "electrical_appliances",
        "transport_mode",
        )
admin.site.register(BaselineHouseholdSurvey, BaselineHouseholdSurveyAdmin)


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
        "opportunistic_illness": admin.VERTICAL,}
admin.site.register(CeaEnrolmentChecklist, CeaEnrolmentChecklistAdmin)


#CsEnrolmentChecklist
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
        "community_resident": admin.VERTICAL,}
admin.site.register(CsEnrolmentChecklist, CsEnrolmentChecklistAdmin)
