from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_supplemental_fields.classes import SupplementalFields, ConditionalFields
from bhp_base_test.models import TestModel
from bhp_base_test.forms import TestModelForm


class TestModelAdmin(BaseModelAdmin):

    form = TestModelForm
    fields = ('f1', 'f2', 'f3', 'f4', 'f5')
    supplimental_fields = SupplementalFields(('f3', 'f4'), p=0.1)

    conditional_fields = ConditionalFields(('f3', ), gender='M', age=(18, 64), bcpp_subject__monthsrecentpartner__first_haart='Yes')

admin.site.register(TestModel, TestModelAdmin)


