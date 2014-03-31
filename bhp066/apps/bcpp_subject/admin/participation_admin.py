from django.contrib import admin

from ..forms import ParticipationForm
from ..models import Participation

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ParticipationAdmin(SubjectVisitModelAdmin):

    form = ParticipationForm
    fields = (
        "subject_visit",
        "full",
        )
    radio_fields = {
        'full': admin.VERTICAL}
admin.site.register(Participation, ParticipationAdmin)
