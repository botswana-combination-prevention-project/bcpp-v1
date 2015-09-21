from django.contrib import admin
from django.utils.translation import ugettext as _

from ..forms import CircumcisionForm, CircumcisedForm, UncircumcisedForm
from ..models import Circumcision, Circumcised, Uncircumcised

from .subject_visit_model_admin import SubjectVisitModelAdmin


class CircumcisionAdmin(SubjectVisitModelAdmin):

    form = CircumcisionForm
    fields = (
        "subject_visit",
        'circumcised',)
    radio_fields = {'circumcised': admin.VERTICAL}
    instructions = [("Note to Interviewer: This section is to be completed "
                     "by male participants. SKIP for female participants. "),
                    _("Read to Participant: Some men are circumcised. "
                      "Male circumcision is [enter site specific word] when "
                      "the foreskin of the man's penis has been cut off. "
                      "I would like to ask you a few questions regarding "
                      "male circumcision.")]
admin.site.register(Circumcision, CircumcisionAdmin)


class CircumcisedAdmin(SubjectVisitModelAdmin):

    form = CircumcisedForm

    baseline_fields = [
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'circ_date',
        'when_circ',
        'age_unit_circ',
        'where_circ',
        'where_circ_other',
        'why_circ',
        'why_circ_other']
    annual_fields = [f for f in baseline_fields if f not in ['when_circ', 'age_unit_circ']]

    baseline_radio_fields = {
        "circumcised": admin.VERTICAL,
        "where_circ": admin.VERTICAL,
        "age_unit_circ": admin.VERTICAL,
        "why_circ": admin.VERTICAL, }

    annual_radio_fields = {
        "circumcised": admin.VERTICAL,
        "where_circ": admin.VERTICAL,
        "why_circ": admin.VERTICAL, }

    filter_horizontal = ("health_benefits_smc",)

admin.site.register(Circumcised, CircumcisedAdmin)


class UncircumcisedAdmin(SubjectVisitModelAdmin):

    form = UncircumcisedForm

    fields = (
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'reason_circ',
        'reason_circ_other',
        'future_circ',
        'future_reasons_smc',
        'service_facilities',
        'aware_free',)
    radio_fields = {
        "circumcised": admin.VERTICAL,
        "reason_circ": admin.VERTICAL,
        "future_circ": admin.VERTICAL,
        "future_reasons_smc": admin.VERTICAL,
        "service_facilities": admin.VERTICAL,
        "aware_free": admin.VERTICAL}
    filter_horizontal = ("health_benefits_smc",)
admin.site.register(Uncircumcised, UncircumcisedAdmin)
