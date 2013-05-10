from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_model_describer.models import Related, GroupingHint


class RelatedAdmin(BaseModelAdmin):

    list_filter = ('app_label', 'model_name')

    list_display = ('app_label', 'model_name', 'field_name', 'related_to_model', 'related_to_field_name')
admin.site.register(Related, RelatedAdmin)


class GroupingHintAdmin(BaseModelAdmin):

    list_filter = ('app_label', 'model_name')

    list_display = ('app_label', 'model_name', 'field_name')
admin.site.register(GroupingHint, GroupingHintAdmin)
