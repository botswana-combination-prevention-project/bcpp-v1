from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import DailyLogForm
from ..models import DailyLog


class DailyLogAdmin(BaseModelAdmin):

    form = DailyLogForm

    fields = (
        'report_date',
        'from_pharma',
        'from_nurse_prescriber',
        'from_ssc',
        'from_other',
        'idcc_scheduled',
        'idcc_newly_registered',
        'idcc_no_shows',
        'approached',
        'refused')

    list_display = (
        'report_date',
        'from_pharma',
        'from_nurse_prescriber',
        'from_ssc',
        'from_other',
        'idcc_scheduled',
        'idcc_newly_registered',
        'idcc_no_shows',
        'approached',
        'refused')

    list_filter = ('report_date', )

admin.site.register(DailyLog, DailyLogAdmin)
