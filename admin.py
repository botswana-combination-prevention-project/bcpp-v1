from django.contrib import admin
from bhp_common.models import MyModelAdmin
from bhp_describer.models import Related

class RelatedAdmin(MyModelAdmin):
    
    list_filter = ('app_label', 'model_name')

    list_display = ('app_label', 'model_name', 'field_name', 'related_to_model', 'related_to_field_name')
admin.site.register(Related, RelatedAdmin)
