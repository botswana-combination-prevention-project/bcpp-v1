from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import SubjectLocatorForm, SubjectDeathForm, RecentPartnerForm, SecondPartnerForm, ThirdPartnerForm


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
