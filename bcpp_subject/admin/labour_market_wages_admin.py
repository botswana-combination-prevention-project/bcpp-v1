from django.contrib import admin
from edc_lib.bhp_base_admin.admin import BaseTabularInline
from bcpp_subject.models import  LabourMarketWages, Grant
from bcpp_subject.forms import LabourMarketWagesForm
from subject_visit_model_admin import SubjectVisitModelAdmin


class GrantInlineAdmin(BaseTabularInline):
    model = Grant


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
