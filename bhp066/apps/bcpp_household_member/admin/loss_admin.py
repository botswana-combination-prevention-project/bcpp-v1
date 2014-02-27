from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..models import HouseholdMember, Loss


class LossAdmin(BaseModelAdmin):

    fields = ('household_member', 'report_datetime', 'reason')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0)):
                household_members = HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0))
            kwargs["queryset"] = household_members
        return super(LossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Loss, LossAdmin)


