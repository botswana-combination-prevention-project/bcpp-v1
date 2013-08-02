from django.contrib import admin
# from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import Uncircumcised
from bcpp_subject.forms import UncircumcisedForm


class UncircumcisedAdmin(SubjectVisitModelAdmin):

    form = UncircumcisedForm
#     supplemental_fields = SupplementalFields(
#         ("circumcised",
#         "health_benefits_smc",
#         'reason_circ',
#         'reason_circ_other',
#         'circumcision_day',
#         'circumcision_day_other',
#         'circumcision_week',
#         'circumcision_week_other',
#         'circumcision_year',
#         'circumcision_year_other',
#         'future_reasons_smc',
#         'service_facilities',
#         'aware_free'), p=0.18, group='MC')
    fields = (
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'reason_circ',
        'reason_circ_other',
        'future_circ',
        'circumcision_day',
        'circumcision_day_other',
        'circumcision_week',
        'circumcision_week_other',
        'circumcision_year',
        'circumcision_year_other',
        'future_reasons_smc',
        'service_facilities',
        'aware_free',)
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
