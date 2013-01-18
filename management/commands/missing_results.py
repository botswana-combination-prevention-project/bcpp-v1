#from django.db.models import F, Q
#from datetime import timedelta
#from lab_clinic_api.models import Result as EdcResult, Panel as EdcPanel
#
#n = 0
#for panel in EdcPanel.objects.all():
#    for visit_definition in VisitDefinition.objects.filter(schedule_group__membership_form__category='maternal').order_by('code'):
#        print visit_definition.code
#        for lab_entry in LabEntry.objects.filter(visit_definition__code=visit_definition.code):
#            print lab_entry
#            if lab_entry.lab_clinic_api_panel.edc_name:
#                for maternal_visit in MaternalVisit.objects.filter(appointment__visit_definition__code=visit_definition.code, appointment__visit_instance=0):
#                    if not EdcResult.objects.filter(order__panel__edc_name=panel_name,
#                                                 order__aliquot__receive__drawn_datetime__gte=maternal_visit.report_datetime.date(),
#                                                 order__aliquot__receive__drawn_datetime__lte=maternal_visit.report_datetime + timedelta(days=5)).exists():
#                        print lab_entry, maternal_visit
#                        n += 1
#
#
#for lab_entry in LabEntry.objects.filter(visit_definition__code=visit_definition.code):
#    print lab_entry
#    if lab_entry.lab_clinic_api_panel.edc_name:
#
#n = 0
#for maternal_visit in MaternalVisit.objects.filter(appointment__visit_definition__code='2000', appointment__visit_instance=0):
#    if not EdcResult.objects.filter(order__panel__edc_name='CD4',
#                                 order__aliquot__receive__drawn_datetime__gte=maternal_visit.report_datetime.date(),
#                                 order__aliquot__receive__drawn_datetime__lte=maternal_visit.report_datetime + timedelta(days=3)).exists():
#        print maternal_visit
#        n += 1
