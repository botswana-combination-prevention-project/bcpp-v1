from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from ..forms import SubjectDeathForm
from ..models import SubjectDeath


class SubjectDeathAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectDeathForm
    fields = (
        'registered_subject',
        'date_death_reported')

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "registered_subject":
#             kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
#         return super(SubjectDeathAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectDeath, SubjectDeathAdmin)
