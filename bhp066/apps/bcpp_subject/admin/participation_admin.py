from django.contrib import admin

from ..forms import ParticipationForm
from ..models import Participation

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ParticipationAdmin(SubjectVisitModelAdmin):

    form = ParticipationForm
    fields = (
        "subject_visit",
        "full",
        "participation_type",
    )
    list_display = ('subject_visit', 'full', 'participation_type')
    list_filter = ('subject_visit', 'full', 'participation_type')
    radio_fields = {
        'full': admin.VERTICAL,
        'participation_type': admin.VERTICAL}
admin.site.register(Participation, ParticipationAdmin)
