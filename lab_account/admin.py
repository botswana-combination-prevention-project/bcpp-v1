from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from lab_account.models import Account


class AccountAdmin(BaseModelAdmin):
    list_per_page = 15
admin.site.register(Account, AccountAdmin)
