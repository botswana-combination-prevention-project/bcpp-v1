from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_visit_tracking.models import TestSubjectVisit


class TestSubjectVisitAdmin(BaseModelAdmin):
    pass
admin.site.register(TestSubjectVisit, TestSubjectVisitAdmin)
