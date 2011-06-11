from django.contrib import admin
from models import ContentTypeMap, MyModelAdmin


class ContentTypeMapAdmin(MyModelAdmin):
    list_display = (  'name', 'content_type','model', 'app_label')
    
    search_fields = ('name', 'app_label', 'model')
    
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)

