from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_identifier.models import SubjectIdentifier, IdentifierTracker, Sequence


class SubjectIdentifierAdmin(BaseModelAdmin):

    list_display = ('identifier', 'created', 'user_created', 'hostname_created')
    search_fields = ('identifier', )
    list_filter = ('created', 'user_created')

admin.site.register(SubjectIdentifier, SubjectIdentifierAdmin)


class IdentifierTrackerAdmin(BaseModelAdmin):

    list_display = ('identifier', 'root_number', 'counter', 'created', 'user_created')
    search_fields = ('identifier', 'root_number')
    list_filter = ('created', 'root_number', 'user_created')

admin.site.register(IdentifierTracker, IdentifierTrackerAdmin)


class SequenceAdmin(BaseModelAdmin):
    list_display = ('pk', 'created', 'user_created', 'hostname_created')
    list_filter = ('created', 'hostname_created', 'user_created')
admin.site.register(Sequence, SequenceAdmin)
