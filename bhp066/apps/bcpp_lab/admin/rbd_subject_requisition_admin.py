from django.contrib import admin

from apps.bcpp_rbd_subject.models import SubjectVisitRBD

from ..classes import SubjectRequisitionModelAdmin
from ..forms import RBDSubjectRequisitionForm
from ..models import RBDSubjectRequisition


class RBDSubjectRequisitionAdmin(SubjectRequisitionModelAdmin):

    visit_model = SubjectVisitRBD
    visit_fieldname = 'subject_visit_rbd'
    dashboard_type = 'rbd_subject'

    form = RBDSubjectRequisitionForm

admin.site.register(RBDSubjectRequisition, RBDSubjectRequisitionAdmin)
