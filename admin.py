from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from bhp_userprofile.models import UserProfile

class UserProfileAdmin(MyModelAdmin):
    list_display = ('user', 'initials')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(UserProfile, UserProfileAdmin)

