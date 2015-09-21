from django.contrib import admin

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin
from edc.export.actions import export_as_csv_action

from bhp066.apps.bcpp_clinic.models import ClinicVisit

from ..actions import print_requisition_label
from ..models import ClinicRequisition, Panel
from ..forms import ClinicRequisitionForm


class ClinicRequisitionAdmin(BaseRequisitionModelAdmin):

    def __init__(self, *args, **kwargs):
        super(ClinicRequisitionAdmin, self).__init__(*args, **kwargs)
        self.list_filter.append('community')

    form = ClinicRequisitionForm
    visit_model = ClinicVisit
    visit_fieldname = 'clinic_visit'
    dashboard_type = 'clinic'

    label_template_name = 'requisition_label'
    actions = [print_requisition_label,
               export_as_csv_action("Export as csv", fields=[], delimiter=',', exclude=['id', 'revision',
                                                                                        'hostname_created',
                                                                                        'hostname_modified',
                                                                                        'user_created',
                                                                                        'user_modified'],)]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                if Panel.objects.get(pk=panel_pk).aliquot_type.all():
                    kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicRequisition, ClinicRequisitionAdmin)
