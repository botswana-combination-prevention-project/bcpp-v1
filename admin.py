from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from django.db.models import Max
from bhp_registration.models import RegisteredSubject
from forms import ScheduledEntryBucketForm
from bhp_entry.models import Entry, ScheduledEntryBucket, AdditionalEntryBucket

class EntryAdmin(MyModelAdmin):

    list_display = ('content_type_map', 'visit_definition', 'entry_order','required', 'entry_category')

admin.site.register(Entry, EntryAdmin)

class ScheduledEntryBucketAdmin(MyModelAdmin):
    
    form = ScheduledEntryBucketForm
    
    list_display = ('registered_subject', 'entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime')

    list_filter = ('entry_status', 'fill_datetime',)

admin.site.register(ScheduledEntryBucket, ScheduledEntryBucketAdmin)

class AdditionalEntryBucketAdmin(MyModelAdmin):
    
    list_display = ('registered_subject', 'content_type_map', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime')

admin.site.register(AdditionalEntryBucket, AdditionalEntryBucketAdmin)


class EntryInline (admin.TabularInline):
    model = Entry
    extra =0
    fields = (
        'content_type_map',
        'entry_order',
        'required',
        'default_entry_status',
        'entry_category',
        'entry_window_calculation',
        'time_point',
        'lower_window',
        'lower_window_unit',
        'upper_window',
        'upper_window_unit',
        
    )
    



