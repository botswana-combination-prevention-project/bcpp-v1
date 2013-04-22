from django.contrib import admin
from bhp_base_model.classes import BaseTabularInline
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner, QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission, HivHealthCareCosts, LabourMarketWages, Grant, BaselineHouseholdSurvey, CeaEnrolmentChecklist, CsEnrolmentChecklist, ResidencyMobility, Demographics, CommunityEngagement, Education, HivTestingHistory, HivTestReview, HivTestingSupplemental, SexualBehaviour, MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner, HivCareAdherence, HivMedicalCare, Circumcision, Circumcised, Uncircumcised
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import SubjectLocatorForm, SubjectDeathForm, RecentPartnerForm, SecondPartnerForm, ThirdPartnerForm, QualityOfLifeForm, ResourceUtilizationForm, OutpatientCareForm, HospitalAdmissionForm, HivHealthCareCostsForm, LabourMarketWagesForm, BaselineHouseholdSurveyForm, CeaEnrolmentChecklistForm, CsEnrolmentChecklistForm, ResidencyMobilityForm, DemographicsForm, CommunityEngagementForm, EducationForm, HivTestingHistoryForm, HivTestReviewForm, HivTestingSupplementalForm, SexualBehaviourForm, MonthsRecentPartnerForm, MonthsSecondPartnerForm, MonthsThirdPartnerForm, HivCareAdherenceForm, HivMedicalCareForm, CircumcisionForm, CircumcisedForm, UncircumcisedForm


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



#ResidentSurvey WIKI
'''
copy the following to your ModelAdmin class in admin.py
class CS002Admin (MyModelAdmin):
    fields = (
        'numberchildren',
        'morechildren',
        'wherecirc',
        'familyplanning',
        'currentpregnant',
        'ancreg',
        'anclastpregnancy',
        'hivlastpregnancy',
        'pregARV',
        'heartattack',
        'heartattackrecord',
        'dxheartattack',
        'cancer',
        'cancerrecord',
        'dxcancer',
        'sti',
        'tb',
        'tbrecord',
        'dxTB',        'circumcised',
        'alcohol',
        'smoke',
        'anticipatestigma',
        'enactedshamestigma',
        'salivastigma',
        'teacherstigma',
        'teacherstigma',
        'testcommunitystigma',
        'gossipcommunitystigma',
        'respectcommunitystigma',
        'enactedverbalstigma',
        'enactedphyicalstigma',
        'enactedfamilystigma',
        'fearstigma',
        'internalize1stigma',
        'internalized2stigma',
        'friendstigma',
        'familystigma',
        'enactedtalkstigma',
        'enactedrespectstigma',
        'enactedjobstigma',
        'whereaccess',
        'whereaccess',
        'overallaccess',
        'emergencyaccess',
        'expensiveaccess',
        'convenientaccess',
        'wheneverlaccess',
        'mobiltyqol',
        'selfcareqol',
        'activitiesqol',
        'painqol',
        'anxietyqol',
        'healthqol',
        'anyvisit3mo',
        'pcvisit3mo',
        'hospvisit3mo',
        'privatevisit3mo',
        'tradvisit3mo',
        'totalvisit3mo',
        'recentvisit',
        'clinic3mo',
        'revisit3mo',
        'costvisit3mo',
        'timetoclinic3mo',
        'transportcosts3mo',
        'otherpaymentcosts3mo',
        'waitcosts',
        'hosp3mo',
        'nightshosp3mo',
        'rehospmo',
        'hospital3mo',
        'recenthospnights3mo',
        'costhosp3mo',
        'timetohosp3mo',
        'transporthosp3mo',
        'otherpaymenthosp3mo',
        'medicines3mo',
        'otherpaymentmeds3mo',
        'hivcarecosts',
        'hivnocarecosts',
        'hivcarelocationcosts',
        'hivcaretimescosts',
        'hivaccompanycosts',
        'employedcosts',
        'occupationcosts',
        'workchangecosts',
        'workdayscosts',
        'workincomecosts',
        'workpaidcosts',
        'householdincomecosts',
        'nonworkactivitiescosts',
        'workpaidcosts',
        'workpaidcosts',
        'nightsawaycosts',
        'weeksawaycosts',
        'dayslostcosts',
        'dayslostadlcosts',
    )
    radio_fields = {
        "morechildren":admin.VERTICAL,
        "wherecirc":admin.VERTICAL,
        "familyplanning":admin.VERTICAL,
        "currentpregnant":admin.VERTICAL,
        "ancreg":admin.VERTICAL,
        "anclastpregnancy":admin.VERTICAL,
        "hivlastpregnancy":admin.VERTICAL,
        "pregARV":admin.VERTICAL,
        "heartattack":admin.VERTICAL,
        "heartattackrecord":admin.VERTICAL,
        "dxheartattack":admin.VERTICAL,
        "cancer":admin.VERTICAL,
        "cancerrecord":admin.VERTICAL,
        "dxcancer":admin.VERTICAL,
        "sti":admin.VERTICAL,
        "tb":admin.VERTICAL,
        "tbrecord":admin.VERTICAL,
        "dxTB":admin.VERTICAL,
        "alcohol":admin.VERTICAL,
        "smoke":admin.VERTICAL,
        "anticipatestigma":admin.VERTICAL,
        "enactedshamestigma":admin.VERTICAL,
        "salivastigma":admin.VERTICAL,
        "teacherstigma":admin.VERTICAL,
        "teacherstigma":admin.VERTICAL,
        "testcommunitystigma":admin.VERTICAL,
        "gossipcommunitystigma":admin.VERTICAL,
        "respectcommunitystigma":admin.VERTICAL,
        "enactedverbalstigma":admin.VERTICAL,
        "enactedphyicalstigma":admin.VERTICAL,
        "enactedfamilystigma":admin.VERTICAL,
        "fearstigma":admin.VERTICAL,
        "internalize1stigma":admin.VERTICAL,
        "internalized2stigma":admin.VERTICAL,
        "friendstigma":admin.VERTICAL,
        "familystigma":admin.VERTICAL,
        "enactedtalkstigma":admin.VERTICAL,
        "enactedrespectstigma":admin.VERTICAL,
        "enactedjobstigma":admin.VERTICAL,
        "whereaccess":admin.VERTICAL,
        "whereaccess":admin.VERTICAL,
        "overallaccess":admin.VERTICAL,
        "emergencyaccess":admin.VERTICAL,
        "expensiveaccess":admin.VERTICAL,
        "convenientaccess":admin.VERTICAL,
        "wheneverlaccess":admin.VERTICAL,
        "mobiltyqol":admin.VERTICAL,
        "selfcareqol":admin.VERTICAL,
        "activitiesqol":admin.VERTICAL,
        "painqol":admin.VERTICAL,
        "anxietyqol":admin.VERTICAL,
        "anyvisit3mo":admin.VERTICAL,
        "pcvisit3mo":admin.VERTICAL,
        "hospvisit3mo":admin.VERTICAL,
        "privatevisit3mo":admin.VERTICAL,
        "tradvisit3mo":admin.VERTICAL,
        "recentvisit":admin.VERTICAL,
        "revisit3mo":admin.VERTICAL,
        "timetoclinic3mo":admin.VERTICAL,
        "otherpaymentcosts3mo":admin.VERTICAL,
        "waitcosts":admin.VERTICAL,
        "rehospmo":admin.VERTICAL,
        "timetohosp3mo":admin.VERTICAL,
        "otherpaymenthosp3mo":admin.VERTICAL,
        "otherpaymentmeds3mo":admin.VERTICAL,
        "hivcarecosts":admin.VERTICAL,
        "hivnocarecosts":admin.VERTICAL,
        "hivcarelocationcosts":admin.VERTICAL,
        "hivcaretimescosts":admin.VERTICAL,
        "hivaccompanycosts":admin.VERTICAL,
        "employedcosts":admin.VERTICAL,
        "occupationcosts":admin.VERTICAL,
        "workincomecosts":admin.VERTICAL,
        "workpaidcosts":admin.VERTICAL,
        "householdincomecosts":admin.VERTICAL,
        "nonworkactivitiescosts":admin.VERTICAL,
        "workpaidcosts":admin.VERTICAL,
        "workpaidcosts":admin.VERTICAL,
        "weeksawaycosts":admin.VERTICAL,
    }
admin.site.register(CS002, CS002Admin)
'''

# ResidencyMobility
class ResidencyMobilityAdmin(SubjectVisitModelAdmin):
 
    form = ResidencyMobilityForm
    fields = (
        "subject_visit",
        'lengthresidence',
        'forteennights',
        'intendresidency',
        'nightsaway',
        'cattlepostlands',
        'reasonaway',)
    radio_fields = {
        "lengthresidence":admin.VERTICAL,
        "forteennights":admin.VERTICAL,
        "intendresidency":admin.VERTICAL,
        "nightsaway":admin.VERTICAL,
        "cattlepostlands":admin.VERTICAL,
        "reasonaway":admin.VERTICAL,}
admin.site.register(ResidencyMobility, ResidencyMobilityAdmin)


#Demographics
class DemographicsAdmin(SubjectVisitModelAdmin):
 
    form = DemographicsForm
    fields = (
        "subject_visit",
        'religion',
        'ethnic',
        'maritalstatus',
        'numwives',
        'livewith',)
    radio_fields = {
        "religion":admin.VERTICAL,
        "ethnic":admin.VERTICAL,
        "maritalstatus":admin.VERTICAL,}
    filter_horizontal = ('livewith',)
admin.site.register(Demographics, DemographicsAdmin)


# CommunityEngagement
class CommunityEngagementAdmin(SubjectVisitModelAdmin):
 
    form = CommunityEngagementForm
    fields = (
        "subject_visit",
        'communityengagement',
        'voteengagement',
        'problemsengagement',
        'solveengagement',)
    radio_fields = {
        "communityengagement":admin.VERTICAL,
        "voteengagement":admin.VERTICAL,
        "solveengagement":admin.VERTICAL,}
    filter_horizontal = ('problemsengagement',)
admin.site.register(CommunityEngagement, CommunityEngagementAdmin)


# Education
class EducationAdmin(SubjectVisitModelAdmin):
 
    form = EducationForm
    fields = (
        "subject_visit",
        'education',
        'employment',
        'moneyforwork',
        'seekingwork',)
    radio_fields = {
        "education":admin.VERTICAL,
        "employment":admin.VERTICAL,
        "moneyforwork":admin.VERTICAL,
        "seekingwork":admin.VERTICAL,}
admin.site.register(Education, EducationAdmin)


# HivTestingHistory
class HivTestingHistoryAdmin(SubjectVisitModelAdmin):
 
    form = HivTestingHistoryForm
    fields = (
        "subject_visit",
        'HHhivtest',
        'whynohivtest',
        'everhivtest',
        'hivtestrecord',)
    radio_fields = {
        "HHhivtest":admin.VERTICAL,
        "whynohivtest":admin.VERTICAL,
        "everhivtest":admin.VERTICAL,
        "hivtestrecord":admin.VERTICAL,}
admin.site.register(HivTestingHistory, HivTestingHistoryAdmin)


#HivTestReview 
class HivTestReviewAdmin(SubjectVisitModelAdmin):
 
    form = HivTestReviewForm
    fields = (
        "subject_visit",
        "hivtestdate",
        'recordedhivresult',
        'whenhivtest',
        'verbalhivresult',)
    radio_fields = {
        "recordedhivresult":admin.VERTICAL,
        "whenhivtest":admin.VERTICAL,
        "verbalhivresult":admin.VERTICAL,}
admin.site.register(HivTestReview, HivTestReviewAdmin)


# HivTestingSupplemental 
class HivTestingSupplementalAdmin(SubjectVisitModelAdmin):
 
    form = HivTestingSupplementalForm
    fields = (
        "subject_visit",
        'numhivtests',
        'wherehivtest',
        'whyhivtest',
        'whynohivtest',
        'hiv_pills',
        'arvshivtest',
        'prefer_hivtest',
        'hivtest_time',
        'hivtest_week',
        'hivtest_year',)
    radio_fields = {
        "wherehivtest":admin.VERTICAL,
        "whyhivtest":admin.VERTICAL,
        "whynohivtest":admin.VERTICAL,
        "hiv_pills":admin.VERTICAL,
        "prefer_hivtest":admin.VERTICAL,
        "whynohivtest":admin.VERTICAL,
        "hivtest_time":admin.VERTICAL,
        "hivtest_week":admin.VERTICAL,
        "hivtest_year":admin.VERTICAL,}
admin.site.register(HivTestingSupplemental, HivTestingSupplementalAdmin)


#SexualBehaviour
class SexualBehaviourAdmin(SubjectVisitModelAdmin):
 
    form = SexualBehaviourForm
    fields = (
        "subject_visit",
        'eversex',
        'lastyearpartners',
        'moresex',
        'firstsex',
        'condom',
        'alcohol_sex',
        'lastsex',
        'lastsex_calc',)
    radio_fields = {
        "eversex":admin.VERTICAL,
        "moresex":admin.VERTICAL,
        "condom":admin.VERTICAL,
        "alcohol_sex":admin.VERTICAL,
        "lastsex":admin.VERTICAL,}
admin.site.register(SexualBehaviour, SexualBehaviourAdmin)


# MonthsRecentPartner 
class MonthsRecentPartnerAdmin(SubjectVisitModelAdmin):
 
    form = MonthsRecentPartnerForm
    fields = (
        "subject_visit",
        'firstpartnerlive',
        'thirdlastsex',
        'firstfirstsex',
        'firstsexcurrent',
        'firstrelationship',
        'firstexchange',
        'concurrent',
        'goods_exchange',
        'firstsexfreq',
        'firstpartnerhiv',
        'firsthaart',
        'firstdisclose',
        'firstcondomfreq',
        'firstpartnercp',)
    radio_fields = {
        "firstpartnerlive":admin.VERTICAL,
        "thirdlastsex":admin.VERTICAL,
        "firstfirstsex":admin.VERTICAL,
        "firstsexcurrent":admin.VERTICAL,
        "firstrelationship":admin.VERTICAL,
        "concurrent":admin.VERTICAL,
        "goods_exchange":admin.VERTICAL,
        "firstpartnerhiv":admin.VERTICAL,
        "firsthaart":admin.VERTICAL,
        "firstdisclose":admin.VERTICAL,
        "firstcondomfreq":admin.VERTICAL,
        "firstpartnercp":admin.VERTICAL,}
admin.site.register(MonthsRecentPartner, MonthsRecentPartnerAdmin)


# MonthsSecondPartner
class MonthsSecondPartnerAdmin(SubjectVisitModelAdmin):
 
    form = MonthsSecondPartnerForm
    fields = (
        "subject_visit",
        'firstpartnerlive',
        'thirdlastsex',
        'firstsexcurrent',
        'firstrelationship',
        'firstexchange',
        'concurrent',
        'goods_exchange',
        'firstsexfreq',
        'firstpartnerhiv',
        'firsthaart',
        'firstdisclose',
        'firstcondomfreq',
        'firstpartnercp',)
    radio_fields = {
        "firstpartnerlive":admin.VERTICAL,
        "thirdlastsex":admin.VERTICAL,
        "firstsexcurrent":admin.VERTICAL,
        "firstrelationship":admin.VERTICAL,
        "concurrent":admin.VERTICAL,
        "goods_exchange":admin.VERTICAL,
        "firstpartnerhiv":admin.VERTICAL,
        "firsthaart":admin.VERTICAL,
        "firstdisclose":admin.VERTICAL,
        "firstcondomfreq":admin.VERTICAL,
        "firstpartnercp":admin.VERTICAL,}
admin.site.register(MonthsSecondPartner, MonthsSecondPartnerAdmin)


#MonthsThirdPartner
class MonthsThirdPartnerAdmin(SubjectVisitModelAdmin):
 
    form = MonthsThirdPartnerForm
    fields = (
        "subject_visit",
        'firstpartnerlive',
        'thirdlastsex',
        'firstsexcurrent',
        'firstrelationship',
        'firstexchange',
        'concurrent',
        'goods_exchange',
        'firstsexfreq',
        'firstpartnerhiv',
        'firsthaart',
        'firstdisclose',
        'firstcondomfreq',
        'firstpartnercp',)
    radio_fields = {
        "firstpartnerlive":admin.VERTICAL,
        "thirdlastsex":admin.VERTICAL,
        "firstsexcurrent":admin.VERTICAL,
        "firstrelationship":admin.VERTICAL,
        "concurrent":admin.VERTICAL,
        "goods_exchange":admin.VERTICAL,
        "firstpartnerhiv":admin.VERTICAL,
        "firsthaart":admin.VERTICAL,
        "firstdisclose":admin.VERTICAL,
        "firstcondomfreq":admin.VERTICAL,
        "firstpartnercp":admin.VERTICAL,}
admin.site.register(MonthsThirdPartner, MonthsThirdPartnerAdmin)


#HivCareAdherence
class HivCareAdherenceAdmin(SubjectVisitModelAdmin):
 
    form = HivCareAdherenceForm
    fields = (
        "subject_visit",
        "firstpositive",
        "medical_care",
        'everrecommendedarv',
        'evertakearv',
        'whynoarv',
        'onarv',
        'arv_stop',
        'adherence4day',
        'adherence4wk',)
    radio_fields = {
        "medical_care":admin.VERTICAL,
        "everrecommendedarv":admin.VERTICAL,
        "evertakearv":admin.VERTICAL,
        "whynoarv":admin.VERTICAL,
        "onarv":admin.VERTICAL,
        "arv_stop":admin.VERTICAL,
        "adherence4day":admin.VERTICAL,
        "adherence4wk":admin.VERTICAL,}
admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
 
 
#HivMedicalCare
class HivMedicalCareAdmin(SubjectVisitModelAdmin):
 
    form = HivMedicalCareForm
    fields = (
        "subject_visit",
        "firsthivcarepositive",
        "lasthivcarepositive",
        'lowestCD4',
        'no_medical_care',)
    radio_fields = {
        "lowestCD4":admin.VERTICAL,
        "no_medical_care":admin.VERTICAL,}
admin.site.register(HivMedicalCare, HivMedicalCareAdmin)


#Circumcision
class CircumcisionAdmin(SubjectVisitModelAdmin):
 
    form = CircumcisionForm
    fields = (
        "subject_visit",
        'circumcised',)
    radio_fields = {
         'circumcised':admin.VERTICAL,}
admin.site.register(Circumcision, CircumcisionAdmin)


#Circumcised
class CircumcisedAdmin(SubjectVisitModelAdmin):
 
    form = CircumcisedForm
    fields = (
        "subject_visit",
        "circumcised",
        "healthbenefitsSMC",
        'whencirc',
        'wherecirc',
        'whycirc',)
    radio_fields = {
        "wherecirc": admin.VERTICAL,
        "whycirc": admin.VERTICAL,}
    filter_horizontal = ("healthbenefitsSMC",)
admin.site.register(Circumcised, CircumcisedAdmin)


#Uncircumcised
class UncircumcisedAdmin(SubjectVisitModelAdmin):

    form = UncircumcisedForm
    fields = (
        "subject_visit",
        "circumcised",
        "healthbenefitsSMC",
        'reasoncirc',
        'futurecirc',
        'circumcision_day',
        'circumcision_week',
        'circumcision_year',
        'futurereasonsSMC',
        'service_facilities',
        'awarefree',
    )
    radio_fields = {
        "reasoncirc":admin.VERTICAL,
        "futurecirc":admin.VERTICAL,
        "circumcision_day":admin.VERTICAL,
        "circumcision_week":admin.VERTICAL,
        "circumcision_year":admin.VERTICAL,
        "futurereasonsSMC":admin.VERTICAL,
        "service_facilities":admin.VERTICAL,
        "awarefree":admin.VERTICAL,}
    filter_horizontal = ("healthbenefitsSMC",)
admin.site.register(Uncircumcised, UncircumcisedAdmin)
