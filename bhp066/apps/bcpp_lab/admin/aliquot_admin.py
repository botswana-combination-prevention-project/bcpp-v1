from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from lis.labeling.actions import print_aliquot_label

from ..actions import create_order
from ..models import Aliquot


class AliquotAdmin(BaseModelAdmin):
    date_hierarchy = 'created'

    actions = [print_aliquot_label, create_order]

    list_display = ("aliquot_identifier", 'subject_identifier', 'processing', 'related', 'to_receive', 'drawn', "aliquot_type", 'aliquot_condition', 'is_packed', 'created', 'user_created', 'hostname_created')

    search_fields = ('aliquot_identifier', 'receive__receive_identifier', 'receive__registered_subject__subject_identifier')

    list_filter = ('aliquot_type', 'aliquot_condition', 'created', 'user_created', 'hostname_created')

    list_per_page = 15

admin.site.register(Aliquot, AliquotAdmin)
