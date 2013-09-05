from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_base_test.models import TestScheduledModel, TestSubjectLocator


class TestScheduledModelAdmin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel, TestScheduledModelAdmin)


class TestSubjectLocatorAdmin(BaseModelAdmin):
    pass
admin.site.register(TestSubjectLocator, TestSubjectLocatorAdmin)
