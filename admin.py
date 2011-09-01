from datetime import *
from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import AliquotCondition, AliquotType

class AliquotTypeAdmin(MyModelAdmin):

    list_display = ('alpha_code', 'numeric_code', 'name', 'created', 'modified')
    
    ordering = ['name']
    
admin.site.register(AliquotType,AliquotTypeAdmin)


class AliquotConditionAdmin(MyModelAdmin):

    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')

    ordering = ['display_index']

admin.site.register(AliquotCondition,AliquotConditionAdmin)

