from django.contrib import admin
#from bhp_site_edc import edc as admin
from bhp_variables.models import StudySpecific, StudySite
from bhp_variables.forms import StudySpecificForm


class StudySpecificAdmin(admin.ModelAdmin):

    form = StudySpecificForm

    list_display = (
        "protocol_number",
        "protocol_code",
        "study_start_datetime",
        "machine_type",
        "hostname_prefix",
        "device_id",
        )

admin.site.register(StudySpecific, StudySpecificAdmin)

admin.site.register(StudySite)
