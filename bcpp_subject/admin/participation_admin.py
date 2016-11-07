from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import ParticipationForm
from ..models import Participation

from .subject_visit_model_admin import SubjectVisitModelAdmin


@admin.register(Participation, site=bcpp_subject_admin)
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
