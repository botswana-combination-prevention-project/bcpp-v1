from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicRefusalForm
from ..models import ClinicRefusal


class ClinicRefusalAdmin(BaseModelAdmin):

    form = ClinicRefusalForm

    fields = ('registration_datetime',
              'refusal_date',
              'site',
              'reason',
              'reason_other',
              'gender',
              'comment')

    list_display = ('registered_subject',
                    'registration_datetime',
                    'user_created',
                    'user_modified',
                    'hostname_created')

    list_filter = ('registration_datetime',
                   'gender',
                   'site',
                   'created',
                   'user_created',
                   'user_modified',
                   'hostname_created')

admin.site.register(ClinicRefusal, ClinicRefusalAdmin)
