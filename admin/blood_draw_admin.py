from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import BloodDraw
from bcpp_subject.forms import BloodDrawForm


class BloodDrawAdmin(SubjectVisitModelAdmin):

    form = BloodDrawForm
    fields = (
        "subject_visit",
        'draw_date',
        'is_blood_drawn',
        'is_blood_drawn_other',)
    radio_fields = {
        'is_blood_drawn': admin.VERTICAL,}
admin.site.register(BloodDraw, BloodDrawAdmin)
