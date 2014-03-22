from django.contrib import admin

from apps.bcpp_subject.models import SubjectVisit

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin


from ..forms import SubjectRequisitionForm
from ..models import SubjectRequisition, Panel


class SubjectRequisitionAdmin(BaseRequisitionModelAdmin):

    visit_model = SubjectVisit
    visit_fieldname = 'subject_visit'
    dashboard_type = 'subject'

    form = SubjectRequisitionForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                if Panel.objects.get(pk=panel_pk).aliquot_type.all():
                    kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectRequisition, SubjectRequisitionAdmin)
