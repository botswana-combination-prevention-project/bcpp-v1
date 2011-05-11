from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from models import GradingList, GradingListItem

class GradingListAdmin(MyModelAdmin):
    pass
admin.site.register(GradingList, GradingListAdmin)


class GradingListItemAdmin(MyModelAdmin):
    list_display = ('test_code', 'gender', 'grade', 'lln', 'uln', 'age_low', 'age_low_unit','age_low_quantifier','age_high','age_high_unit','age_high_quantifier', 'panic_value_low', 'panic_value_high', 'grading_list')
    search_fields = ['grading_list', 'grade', 'test_code__code','test_code__name',]
admin.site.register(GradingListItem, GradingListItemAdmin)

