from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ReproductiveHealthAdmin(SubjectVisitModelAdmin):

    form = ReproductiveHealthForm
    annual_fields = [
        "subject_visit",
        "number_children",
        "menopause",
        "family_planning",
        "family_planning_other",
        'currently_pregnant',
        'when_pregnant',
        'gestational_weeks',
        'pregnancy_hiv_tested',
        'pregnancy_hiv_retested']

    baseline_fields = [f for f in annual_fields if f not in [
        "when_pregnant", "gestational_weeks", "pregnancy_hiv_tested", "pregnancy_hiv_retested"]]

    annual_radio_fields = {
        "menopause": admin.VERTICAL,
        "currently_pregnant": admin.VERTICAL,
        "when_pregnant": admin.VERTICAL,
        "pregnancy_hiv_tested": admin.VERTICAL,
        "pregnancy_hiv_retested": admin.VERTICAL
    }

    baseline_radio_fields = {
        "menopause": admin.VERTICAL,
        "currently_pregnant": admin.VERTICAL,
        "when_pregnant": admin.VERTICAL,
        "pregnancy_hiv_tested": admin.VERTICAL,
        "pregnancy_hiv_retested": admin.VERTICAL}

    filter_horizontal = ("family_planning",)
    instructions = [("<h5>Note to Interviewer</h5> This section is to be"
                     " completed by female participants. SKIP for male participants."),
                    _("Read to Participant: I am now going to ask you questions"
                      " about reproductive health and pregnancy.")]

admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)
