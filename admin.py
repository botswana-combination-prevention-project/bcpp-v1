from django.contrib import admin
from models import ContentTypeMap, MyModelAdmin
from models import IdentifierTracker

class ContentTypeMapAdmin(MyModelAdmin):
    list_display = (  'name', 'content_type','model', 'app_label')
    
    search_fields = ('name', 'app_label', 'model')
    
    list_filter = ('app_label',)
    
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)

class IdentifierTrackerAdmin(MyModelAdmin):

    list_display = (  'identifier', 'root_number','counter', 'created')
    
    search_fields = ('identifier', 'root_number')
    
    list_filter = ('created',)
    
admin.site.register(IdentifierTracker, IdentifierTrackerAdmin)
