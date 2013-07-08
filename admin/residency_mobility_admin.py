from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import ResidencyMobility
from bcpp_subject.forms import ResidencyMobilityForm


class ResidencyMobilityAdmin(SubjectVisitModelAdmin):

    form = ResidencyMobilityForm
    fields = (
        "subject_visit",
        'length_residence',
        'forteen_nights',
        'intend_residency',
        'nights_away',
        'cattle_postlands',
        'cattle_postlands_other')
    radio_fields = {
        "length_residence": admin.VERTICAL,
        "forteen_nights": admin.VERTICAL,
        "intend_residency": admin.VERTICAL,
        "nights_away": admin.VERTICAL,
        "cattle_postlands": admin.VERTICAL}
admin.site.register(ResidencyMobility, ResidencyMobilityAdmin)
