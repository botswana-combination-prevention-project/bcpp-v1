from django.contrib import admin
from models import ContentTypeMap, MyModelAdmin


class ContentTypeMapAdmin(MyModelAdmin):
    list_display = ( 'content_type', 'name', 'model', 'app_label')
    
    search_fields = ('name', 'app_label', )
    
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)

