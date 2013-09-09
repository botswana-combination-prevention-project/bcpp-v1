from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_userprofile.models import UserProfile


class UserProfileAdmin(BaseModelAdmin):
    list_display = ('user', 'initials')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(UserProfile, UserProfileAdmin)
