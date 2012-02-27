from django.contrib import admin
from bhp_variables.models import StudySpecific, StudySite
from forms import StudySpecificForm


class StudySpecificAdmin(admin.ModelAdmin):
    
    form = StudySpecificForm
    
    list_display = (
        "protocol_number", 
        "study_start_datetime",
        "machine_type",
        "hostname_prefix",
        "device_id",
        )

admin.site.register(StudySpecific, StudySpecificAdmin)

admin.site.register(StudySite)


