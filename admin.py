from django.contrib import admin
from models import StudySpecific, StudySite, StudySpecificSetting

admin.site.register(StudySpecific)

admin.site.register(StudySite)

class StudySpecificSettingAdmin (admin.ModelAdmin):
    list_display = (
        'setting_keyword',
        'setting_value',
    )

admin.site.register(StudySpecificSetting, StudySpecificSettingAdmin)

