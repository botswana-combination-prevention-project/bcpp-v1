from django.contrib import admin

from edc.base.admin.admin import BaseTabularInline

from edc.lab.lab_profile.admin import BaseProfileAdmin, BaseProfileItemAdmin

from ..models import ProfileItem, Profile


class ProfileItemAdmin(BaseProfileItemAdmin):
    pass
admin.site.register(ProfileItem, ProfileItemAdmin)


class ProfileItemInlineAdmin(BaseTabularInline):
    model = ProfileItem


class ProfileAdmin(BaseProfileAdmin):
    inlines = [ProfileItemInlineAdmin]
admin.site.register(Profile, ProfileAdmin)
