from django.contrib import admin
from bhp_crypto.classes import BaseCryptorModelAdmin as BaseModelAdmin
from models import RegisteredSubject, SubjectIdentifierAuditTrail
from forms import RegisteredSubjectForm


class SubjectIdentifierAuditTrailAdmin(BaseModelAdmin):

    list_display = (
        'subject_identifier',
        'date_allocated',
        )
    list_per_page = 15

admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)
