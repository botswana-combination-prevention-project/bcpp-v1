from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from bhp_lab_test_code.models import TestCode, TestCodeGroup, TestCodeReferenceList, TestCodeReferenceListItem, TestCodeInterfaceMapping

class TestCodeAdmin(MyModelAdmin):
    list_display = ('code', 'name', 'test_code_group', 'units', 'display_decimal_places', 'reference_range_lo', 'reference_range_hi', 'lln', 'uln')
admin.site.register(TestCode, TestCodeAdmin)

class TestCodeReferenceListAdmin(MyModelAdmin):
    pass
admin.site.register(TestCodeReferenceList, TestCodeReferenceListAdmin)    
    
class TestCodeReferenceListItemAdmin(MyModelAdmin):
    list_display = ('test_code', 'gender', 'lln', 'uln', 'age_low', 'age_low_unit','age_low_quantifier','age_high','age_high_unit','age_high_quantifier', 'panic_value', 'panic_value_quantifier', 'test_code_reference_list')
    search_fields = ['test_code_reference_list', 'test_code__code','test_code__name',]
admin.site.register(TestCodeReferenceListItem, TestCodeReferenceListItemAdmin)

class TestCodeInterfaceMappingAdmin(MyModelAdmin):
    pass
admin.site.register(TestCodeInterfaceMapping, TestCodeInterfaceMappingAdmin)

class TestCodeGroupAdmin(MyModelAdmin):
    pass
admin.site.register(TestCodeGroup, TestCodeGroupAdmin)

