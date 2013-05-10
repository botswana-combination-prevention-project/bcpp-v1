from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_visit_tracking.models import TestSubjectVisit


class TestSubjectVisitAdmin(BaseModelAdmin):
    pass
admin.site.register(TestSubjectVisit, TestSubjectVisitAdmin)
