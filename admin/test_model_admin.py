from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_supplimental_fields.classes import SupplimentalFields
from bhp_base_test.models import TestModel
from bhp_base_test.forms import TestModelForm


class TestModelAdmin(BaseModelAdmin):

    form = TestModelForm
    fields = ('f1', 'f2', 'f3', 'f4', 'f5')
    supplimental_fields = SupplimentalFields(('f3', 'f4'), p=0.5)

admin.site.register(TestModel, TestModelAdmin)
