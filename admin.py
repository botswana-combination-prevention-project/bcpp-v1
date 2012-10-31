from django.contrib import admin
#from bhp_export_data.actions import export_as_csv_action
from bhp_base_model.classes import BaseModelAdmin
from actions import flag_as_active, flag_as_inactive
from models import GradingList, GradingListItem, ReferenceRangeList, ReferenceRangeListItem


class GradingListAdmin(BaseModelAdmin):
    pass
admin.site.register(GradingList, GradingListAdmin)


class GradingListItemAdmin(BaseModelAdmin):
    list_display = ('test_code', 'grade', 'active', 'describe', 'hiv_status', 'gender', 'value_low', 'value_high', 'age_low', 'age_low_unit', 'age_low_quantifier',
                    'age_high', 'age_high_unit', 'age_high_quantifier', 'grading_list', 'scale')
    search_fields = ['grade', 'test_code__code', 'test_code__name', 'value_low', 'value_high', 'hiv_status']
    list_filter = ('grade', 'hiv_status', 'grading_list', 'scale', 'active', 'test_code')
    actions = [flag_as_active, flag_as_inactive]
admin.site.register(GradingListItem, GradingListItemAdmin)


class ReferenceRangeListAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferenceRangeList, ReferenceRangeListAdmin)


class ReferenceRangeListItemAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferenceRangeListItem, ReferenceRangeListItemAdmin)
