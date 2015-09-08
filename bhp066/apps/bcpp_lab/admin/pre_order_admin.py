from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import PreOrder


class PreOrderAdmin(BaseModelAdmin):

    list_display = ('subject_visit', 'panel', 'preorder_datetime', 'status', 'aliquot_identifier')
    list_filter = ('panel', 'preorder_datetime', 'status',)
    search_fields = ('status', 'ssubject_visit__subject_identifier')
    list_editable = ('aliquot_identifier', )

admin.site.register(PreOrder, PreOrderAdmin)