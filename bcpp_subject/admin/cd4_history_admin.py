from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import Cd4History
from bcpp_subject.forms import Cd4HistoryForm


class Cd4HistoryAdmin(SubjectVisitModelAdmin):

    form = Cd4HistoryForm
    fields = (
        "subject_visit",
        'record_available',
        'last_cd4_count',
        'last_cd4_drawn_date',)
    radio_fields = {
        'record_available': admin.VERTICAL,}
admin.site.register(Cd4History, Cd4HistoryAdmin)
