from django.contrib import admin
from bcpp_subject.models import SubjectDeath
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.forms import SubjectDeathForm


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
