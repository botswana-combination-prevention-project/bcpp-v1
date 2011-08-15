from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import IdentifierTracker



class IdentifierTrackerAdmin(MyModelAdmin):

    list_display = (  'identifier', 'root_number','counter', 'created')
    
    search_fields = ('identifier', 'root_number')
    
    list_filter = ('created',)
    
admin.site.register(IdentifierTracker, IdentifierTrackerAdmin)
