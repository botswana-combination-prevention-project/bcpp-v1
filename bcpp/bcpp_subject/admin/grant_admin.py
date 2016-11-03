from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline, BaseModelAdmin

from ..forms import GrantForm
from ..models import LabourMarketWages, Grant


class GrantAdmin(BaseModelAdmin):
    form = GrantForm
    fields = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant',)
    list_display = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "labour_market_wages":
            kwargs["queryset"] = LabourMarketWages.objects.filter(id__exact=request.GET.get('labour_market_wages', 0))
        return super(GrantAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Grant, GrantAdmin)


class GrantInlineAdmin(BaseTabularInline):
    model = Grant
    form = GrantForm
    extra = 1
    fields = ('grant_number', 'grant_type', 'other_grant',)
    list_display = ('grant_number', 'grant_type', 'other_grant', )
