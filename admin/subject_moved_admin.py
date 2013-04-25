from django.contrib import admin
from bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.models import SubjectMoved
from bcpp_subject.forms import SubjectMovedForm


class SubjectMovedAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectMovedForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'registered_subject',
        'household_structure_member',
        'report_datetime',
        'moved_date',
        'moved_reason',
        'moved_reason_other',
        'place_moved',
        'area_moved',
        'contact_details',
        'comment')
    list_display = (
        'household_structure_member', 
        'moved_reason')
    search_fields = [
        'household_structure_member__first_name', 
        'household_structure_member__household_structure__household__household_identifier']
    list_filter = ('survey',)
    radio_fields = {
        "moved_reason": admin.VERTICAL,
        "place_moved": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure_member":
            kwargs["queryset"] = HouseholdStructureMember.objects.filter(id__exact=request.GET.get('household_structure_member', 0))
        return super(SubjectMovedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(SubjectMoved, SubjectMovedAdmin)
