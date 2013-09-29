from django.contrib import admin
from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm
from . import SubjectVisitModelAdmin


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
                             ("Read to Participant: I am now going to ask you questions"
                             " about reproductive health and pregnancy.")]
admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)
