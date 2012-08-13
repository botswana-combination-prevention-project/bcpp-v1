from django.contrib import admin
#from bhp_export_data.actions import export_as_csv_action
from bhp_base_model.classes import BaseModelAdmin
from models import GradingList, GradingListItem, ReferenceRangeList, ReferenceRangeListItem


class GradingListAdmin(BaseModelAdmin):
    pass
admin.site.register(GradingList, GradingListAdmin)


class GradingListItemAdmin(BaseModelAdmin):
    pass
admin.site.register(GradingListItem, GradingListItemAdmin)


class ReferenceRangeListAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferenceRangeList, ReferenceRangeListAdmin)


class ReferenceRangeListItemAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferenceRangeListItem, ReferenceRangeListItemAdmin)
