from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ReproductiveHealthAdmin(SubjectVisitModelAdmin):

    form = ReproductiveHealthForm
    fields = (
        "subject_visit",
        "number_children",
        "menopause",
        "family_planning",
        "family_planning_other",
        "currently_pregnant",
        )
    radio_fields = {
        "menopause": admin.VERTICAL,
        "currently_pregnant": admin.VERTICAL}
    filter_horizontal = ("family_planning",)
    instructions = [("Note to Interviewer: This section is to be"
                             " completed by female participants. SKIP for male participants."),
                             _("Read to Participant: I am now going to ask you questions"
                             " about reproductive health and pregnancy.")]
admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)
