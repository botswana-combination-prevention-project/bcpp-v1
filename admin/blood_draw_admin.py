from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import BloodDraw
from bcpp_subject.forms import BloodDrawForm


class BloodDrawAdmin(SubjectVisitModelAdmin):

    form = BloodDrawForm
    fields = (
        "subject_visit",
        'is_blood_drawn',
        'is_blood_drawn_other',
        'draw_date',
        'record_available',
        'last_cd4_count',
        'last_cd4_drawn_date',)
    radio_fields = {
        'is_blood_drawn': admin.VERTICAL,
        'record_available': admin.VERTICAL,}
admin.site.register(BloodDraw, BloodDrawAdmin)
