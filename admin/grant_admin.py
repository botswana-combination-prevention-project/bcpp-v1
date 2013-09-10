from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_subject.models import Grant


class GrantAdmin(BaseModelAdmin):
    pass
admin.site.register(Grant, GrantAdmin)
