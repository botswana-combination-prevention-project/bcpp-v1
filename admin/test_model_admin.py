from django.contrib import admin
from bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_base_model.models import TestModel, TestManyToMany, TestForeignKey


class TestModelAdmin(BaseRegisteredSubjectModelAdmin):

    pass

admin.site.register(TestModel, TestModelAdmin)


class TestManyToManyAdmin(BaseModelAdmin):

    pass

admin.site.register(TestManyToMany, TestManyToManyAdmin)


class TestForeignKeyAdmin(BaseModelAdmin):

    pass

admin.site.register(TestForeignKey, TestForeignKeyAdmin)
