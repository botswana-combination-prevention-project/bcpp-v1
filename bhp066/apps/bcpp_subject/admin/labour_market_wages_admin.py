from django.contrib import admin

from edc.base.modeladmin.admin import BaseTabularInline, BaseModelAdmin

from ..forms import LabourMarketWagesForm, GrantForm
from ..models import LabourMarketWages, Grant

from .subject_visit_model_admin import SubjectVisitModelAdmin


class GrantAdmin(BaseModelAdmin):
    form = GrantForm
    fields = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant',)
    list_display = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant', )
    search_fields = ('labour_market_wages__subject_visit__appointment__registered_subject__subject_identifier',)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "labour_market_wages":
#             if request.GET.get('labour_market_wages')
#                 kwargs["queryset"] = LabourMarketWages.objects.filter(id=request.GET.get('labour_market_wages'))
#
#         return super(GrantAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Grant, GrantAdmin)


class GrantInlineAdmin(BaseTabularInline):
    model = Grant
    form = GrantForm
    extra = 1


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
