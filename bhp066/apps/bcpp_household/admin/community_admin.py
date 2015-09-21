from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import Community


class CommunityAdmin(BaseModelAdmin):
    instructions = []

admin.site.register(Community, CommunityAdmin)
