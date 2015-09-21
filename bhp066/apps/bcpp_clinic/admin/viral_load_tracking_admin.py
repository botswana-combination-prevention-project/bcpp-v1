from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ViralLoadTrackingForm
from ..models import ViralLoadTracking


class ViralLoadTrackingAdmin(BaseModelAdmin):

    form = ViralLoadTrackingForm
    fields = ('clinic_visit',
              'report_datetime',
              'is_drawn',
              'reason_not_drawn',
              'drawn_datetime',
              'clinician_initials',)
    list_display = ('clinic_visit', 'is_drawn', 'reason_not_drawn', 'drawn_datetime')
    list_filter = ('is_drawn',)
admin.site.register(ViralLoadTracking, ViralLoadTrackingAdmin)
