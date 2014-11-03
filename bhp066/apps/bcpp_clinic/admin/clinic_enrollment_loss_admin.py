from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicEnrollmentLossForm
from ..models import ClinicEnrollmentLoss


class ClinicEnrollmentLossAdmin(BaseModelAdmin):

    form = ClinicEnrollmentLossForm

    fields = ('registration_datetime', 'reason')

    list_display = ('registered_subject', 'registration_datetime', 'user_created', 'user_modified', 'hostname_created')

    list_filter = ('registration_datetime', 'user_created', 'user_modified', 'hostname_created')

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "registered_subject":
#             registered_subject = RegisteredSubject.objects.none()
#             if RegisteredSubject.objects.filter(household_structure__exact=request.GET.get('household_structure', 0)):
#                 registered_subject = RegisteredSubject.objects.filter(household_structure__exact=request.GET.get('household_structure', 0))
#             kwargs["queryset"] = registered_subject
#         return super(ClinicEnrollmentLossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicEnrollmentLoss, ClinicEnrollmentLossAdmin)
