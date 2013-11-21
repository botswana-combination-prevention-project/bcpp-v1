from django.contrib import admin
from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin
from apps.bcpp_household_member.models import HouseholdMember
from ..models import SubjectMoved
from ..forms import SubjectMovedForm


class SubjectMovedAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectMovedForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'registered_subject',
        'household_member',
        'report_datetime',
        'moved_date',
        'moved_reason',
        'moved_reason_other',
        'place_moved',
        'area_moved',
        'contact_details',
        'comment')
    list_display = (
        'household_member',
        'moved_reason')
    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']
    list_filter = ('survey',)
    radio_fields = {
        "moved_reason": admin.VERTICAL,
        "place_moved": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('HouseholdMember', 0))
        return super(SubjectMovedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectMoved, SubjectMovedAdmin)
