from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import Grant


class GrantAdmin(BaseModelAdmin):
    pass
admin.site.register(Grant, GrantAdmin)
