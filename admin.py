from django.contrib import admin
from bhp_common.models import MyModelAdmin
from bhp_identifier.models import IdentifierTracker


class IdentifierTrackerAdmin(MyModelAdmin):

    list_display = ('identifier', 'root_number', 'counter', 'created', 'user_created')
    search_fields = ('identifier', 'root_number')
    list_filter = ('created', 'root_number', 'user_created')

admin.site.register(IdentifierTracker, IdentifierTrackerAdmin)
