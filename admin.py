from django.contrib import admin
from bhp_common.models import MyModelAdmin
from bhp_model_describer.models import Related, GroupingHint

class RelatedAdmin(MyModelAdmin):
    
    list_filter = ('app_label', 'model_name')

    list_display = ('app_label', 'model_name', 'field_name', 'related_to_model', 'related_to_field_name')
admin.site.register(Related, RelatedAdmin)

class GroupingHintAdmin(MyModelAdmin):
    
    list_filter = ('app_label', 'model_name')

    list_display = ('app_label', 'model_name', 'field_name')
admin.site.register(GroupingHint, GroupingHintAdmin)
