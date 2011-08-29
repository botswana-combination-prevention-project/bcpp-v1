from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_lab_account.models import Account

class AccountAdmin(MyModelAdmin):

    """
    filter_horizontal= (
        'principal_investigator',
        'site_leader',
    ) 
    """
    list_per_page = 15
    
admin.site.register(Account, AccountAdmin)

