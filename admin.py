from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import ContentTypeMap
# Add any missing content types
from django.contrib.contenttypes.management \
    import update_all_contenttypes


def pop_and_sync(modeladmin, request, queryset):
    update_all_contenttypes()
    ContentTypeMap.objects.populate()
    ContentTypeMap.objects.sync()    
pop_and_sync.short_description = "Re-populate and sync content type"


class ContentTypeMapAdmin(MyModelAdmin):
    list_display = (  'name', 'content_type','model', 'app_label')
    
    search_fields = ('name', 'app_label', 'model')
    
    list_filter = ('app_label',)
    
    actions = [pop_and_sync,]
    
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)


