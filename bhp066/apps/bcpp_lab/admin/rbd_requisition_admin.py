from django.contrib import admin

from apps.bcpp_rbd.models import RBDVisit

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from ..forms import RBDRequisitionForm
from ..models import RBDRequisition


class RBDRequisitionAdmin(BaseRequisitionModelAdmin):

    visit_model = RBDVisit
    visit_fieldname = 'rbd_visit'
    dashboard_type = 'subject'

    form = RBDRequisitionForm

admin.site.register(RBDRequisition, RBDRequisitionAdmin)
