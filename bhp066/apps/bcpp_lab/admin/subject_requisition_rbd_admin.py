from django.contrib import admin

from apps.bcpp_rbd_subject.models import SubjectVisitRBD

from ..classes import SubjectRequisitionModelAdmin
from ..forms import SubjectRequisitionRBDForm
from ..models import SubjectRequisitionRBD


class SubjectRequisitionRBDAdmin(SubjectRequisitionModelAdmin):

    visit_model = SubjectVisitRBD
    visit_fieldname = 'subject_visit_rbd'
    dashboard_type = 'rbd_subject'

    form = SubjectRequisitionRBDForm

admin.site.register(SubjectRequisitionRBD, SubjectRequisitionRBDAdmin)
