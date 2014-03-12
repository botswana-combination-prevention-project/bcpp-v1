from django.contrib import admin

from apps.bcpp_rbd.models import RBDVisit

from ..classes import SubjectRequisitionModelAdmin
from ..forms import SubjectRequisitionRBDForm
from ..models import SubjectRequisitionRBD


class SubjectRequisitionRBDAdmin(SubjectRequisitionModelAdmin):

    visit_model = RBDVisit
    visit_fieldname = 'rbd_visit'
    dashboard_type = 'rbd_subject'

    form = SubjectRequisitionRBDForm

admin.site.register(SubjectRequisitionRBD, SubjectRequisitionRBDAdmin)
