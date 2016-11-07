from django.contrib import admin


from ..admin_site import bcpp_household_member_admin
from ..forms import EnrollmentLossForm
from ..models import HouseholdMember, EnrollmentLoss

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(EnrollmentLoss, site=bcpp_household_member_admin)
class EnrollmentLossAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    form = EnrollmentLossForm

    fields = ('household_member', 'report_datetime', 'reason')

    list_display = ('report_datetime', 'user_created', 'user_modified', 'hostname_created')

    list_filter = ('report_datetime', 'user_created', 'user_modified', 'hostname_created',
                   'household_member__household_structure__household__community')

    instructions = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0)):
                household_members = HouseholdMember.objects.filter(
                    household_structure__exact=request.GET.get('household_structure', 0))
            kwargs["queryset"] = household_members
        return super(EnrollmentLossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
