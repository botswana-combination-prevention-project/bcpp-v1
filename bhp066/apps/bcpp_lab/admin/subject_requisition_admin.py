from django.contrib import admin

from edc.export.actions import export_as_csv_action
from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from bhp066.apps.bcpp_subject.models import SubjectVisit

from ..actions import print_requisition_label
from ..filters import PocViralLoadRequsitions
from ..forms import SubjectRequisitionForm
from ..models import SubjectRequisition, Panel


class SubjectRequisitionAdmin(BaseRequisitionModelAdmin):

    visit_model = SubjectVisit
    visit_attr = 'subject_visit'

    def __init__(self, *args, **kwargs):
        super(SubjectRequisitionAdmin, self).__init__(*args, **kwargs)
        self.list_filter.append('community')
        self.list_filter.append(PocViralLoadRequsitions)
        self.list_display.append('is_pov_vl')

    visit_model = SubjectVisit
    visit_fieldname = 'subject_visit'
    dashboard_type = 'subject'

    form = SubjectRequisitionForm
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

admin.site.register(SubjectRequisition, SubjectRequisitionAdmin)
