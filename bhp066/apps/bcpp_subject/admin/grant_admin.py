from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from ..models import Grant


class GrantAdmin(BaseModelAdmin):
    pass
admin.site.register(Grant, GrantAdmin)
