from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import PreOrderForm
from ..models import PreOrder


class PreOrderAdmin(BaseModelAdmin):
    form = PreOrderForm

    fields = ('panel', 'aliquot_identifier', 'preorder_datetime', 'status')
    list_display = ('subject_visit', 'panel', 'preorder_datetime', 'status', 'aliquot_identifier', 'result')
    list_filter = ('panel', 'preorder_datetime', 'status',)
    search_fields = ('status', 'subject_visit__subject_identifier')
    readonly_fields = ('status', )

admin.site.register(PreOrder, PreOrderAdmin)
