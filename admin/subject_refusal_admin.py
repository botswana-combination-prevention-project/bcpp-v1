from django.contrib import admin
from bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.models import SubjectRefusal
from bcpp_subject.forms import SubjectRefusalForm


class SubjectRefusalAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectRefusalForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'registered_subject', 
        'household_structure_member', 
        'report_datetime',
        'sex',
        'age',
        'lengthresidence',
        'refusal_date', 
        'whynoparticipate',
        'whynoparticipate_other',
#         'subject_refusal_status',
        'hivtesttoday',
        'whynohivtest',
        'comment')
    
    radio_fields = {
        "sex":admin.VERTICAL,
        "lengthresidence":admin.VERTICAL,
        "whynoparticipate":admin.VERTICAL,
        "hivtesttoday":admin.VERTICAL,
        "whynohivtest":admin.VERTICAL,}
    
    list_display = (
        'household_structure_member', 
        'whynoparticipate')
    
    search_fields = [
        'household_structure_member__first_name',
        'household_structure_member__household_structure__household__household_identifier']
    
    list_filter = (
        'survey', 
        'whynoparticipate')
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure_member":
            kwargs["queryset"] = HouseholdStructureMember.objects.filter(id__exact=request.GET.get('household_structure_member', 0))
        return super(SubjectRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(SubjectRefusal, SubjectRefusalAdmin)
