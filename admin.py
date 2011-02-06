from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_consent.models import SubjectIdentifierAuditTrail

class SubjectIdentifierAuditTrailAdmin(MyModelAdmin):
    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'date_allocated',
        )
    list_per_page = 15
        
admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)

