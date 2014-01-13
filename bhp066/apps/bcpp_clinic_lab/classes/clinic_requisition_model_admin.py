from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin
from apps.bcpp_clinic.models import ClinicVisit


class ClinicRequisitionModelAdmin (BaseRequisitionModelAdmin):

    visit_model = ClinicVisit
    visit_fieldname = 'clinic_visit'
    dashboard_type = 'subject'
