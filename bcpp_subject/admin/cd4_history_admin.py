from django.contrib import admin

from ..models import Cd4History
from ..forms import Cd4HistoryForm

from .modeladmin_mixins import CrfModelAdminMixin


class Cd4HistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = Cd4HistoryForm
    fields = (
        "subject_visit",
        'record_available',
        'last_cd4_count',
        'last_cd4_drawn_date',)
    radio_fields = {
        'record_available': admin.VERTICAL}
admin.site.register(Cd4History, Cd4HistoryAdmin)
