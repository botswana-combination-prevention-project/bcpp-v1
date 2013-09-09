from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from audit_trail.models import AuditComment


class AuditCommentAdmin(BaseModelAdmin):

    list_filter = ('audit_subject_identifier', 'app_label', 'model_name', )
    list_display = ('audit_subject_identifier', 'audit_id', 'app_label', 'model_name',)
    #readonly_fields = ('audit_subject_identifier', 'audit_id', 'app_label', 'model_name',)

admin.site.register(AuditComment, AuditCommentAdmin)
