from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_subject_config.models import SubjectConfiguration
from bhp_subject_config.forms import SubjectConfigurationForm


class SubjectConfigurationAdmin(BaseModelAdmin):
    form = SubjectConfigurationForm

    list_display = ('subject_identifier', 'default_appt_type')
    search_fields = ('subject_identifier', )
    list_filter = ('default_appt_type', )
admin.site.register(SubjectConfiguration, SubjectConfigurationAdmin)
