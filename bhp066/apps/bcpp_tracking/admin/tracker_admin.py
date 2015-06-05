from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from apps.bcpp_household.models import SiteTracker, Tracker
from apps.bcpp_household.forms import TrackerForm, SiteTrackerForm


class SiteTrackerAdmin(BaseModelAdmin):
    form = SiteTrackerForm
    fields = ('end_date', 'start_date', 'tracked_value', 'site_name', 'model', 'app_name', 'update_date', 'tracker', 'value_limit')
    list_per_page = 15
    list_display = ('tracked_value', 'site_name', 'update_date', 'tracker')
    list_filter = ('end_date', 'start_date', 'tracked_value', 'site_name', 'update_date')
    search_fields = ('site_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tracker":
            kwargs["queryset"] = Tracker.objects.filter(id__exact=request.GET.get('tracker', 0))
        return super(SiteTrackerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Tracker, SiteTrackerAdmin)


class SiteTrackerInline(admin.TabularInline):
    model = SiteTracker
    extra = 0
    max_num = 5


class TrackerAdmin(BaseModelAdmin):
    form = TrackerForm
    instructions = []
    inlines = [SiteTrackerInline, ]
    date_hierarchy = 'modified'
    list_per_page = 15
    list_display = ('end_date', 'start_date', 'tracked_value', 'model', 'app_name', 'update_date', 'tracker', 'value_limit')
    list_filter = ('end_date', 'start_date', 'update_date')
admin.site.register(Tracker, TrackerAdmin)
