from django.contrib import admin
from bhp_variables.models import StudySpecific, StudySite

class StudySpecificAdmin(admin.ModelAdmin):
    
    list_display = (
        "protocol_number", 
        "study_start_datetime",
        "hostname_prefix",
        "device_id",
        )

admin.site.register(StudySpecific, StudySpecificAdmin)

admin.site.register(StudySite)


