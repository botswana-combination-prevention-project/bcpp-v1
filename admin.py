from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import DxCode

class DxCodeAdmin(MyModelAdmin):

    list_display = ('code', 'short_name')
    
    search_fields = ('code', 'short_name', 'long_name')
    
    #readonly_fields = ('code', 'short_name', 'long_name')
   
admin.site.register(DxCode, DxCodeAdmin)

