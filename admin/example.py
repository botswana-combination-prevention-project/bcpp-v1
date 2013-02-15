#from django.contrib import admin
#from bhp_common.models import MyTabularInline
#from maikalelo_infant.admin import InfantVisitModelAdmin
#from maikalelo_infant.models import InfantContactLog, InfantContactLogItem
#from maikalelo_infant.forms import InfantContactLogItemForm
#
#
#class InfantContactLogItemInlineAdmin(MyTabularInline):
#
#    model = InfantContactLogItem
#    form = InfantContactLogItemForm
#    extras = 1
#    radio_fields = {"is_contacted": admin.VERTICAL,
#                    "infant_status": admin.VERTICAL}
#
#
#class InfantContactLogAdmin(InfantVisitModelAdmin):
#
#    inlines = [InfantContactLogItemInlineAdmin, ]
#admin.site.register(InfantContactLog, InfantContactLogAdmin)
