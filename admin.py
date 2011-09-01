from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import ContentTypeMap


class ContentTypeMapAdmin(MyModelAdmin):
    list_display = (  'name', 'content_type','model', 'app_label')
    
    search_fields = ('name', 'app_label', 'model')
    
    list_filter = ('app_label',)
    
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)


