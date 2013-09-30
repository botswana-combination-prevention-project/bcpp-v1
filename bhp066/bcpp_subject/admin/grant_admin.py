from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin
from ..models import Grant


class GrantAdmin(BaseModelAdmin):
    pass
admin.site.register(Grant, GrantAdmin)
