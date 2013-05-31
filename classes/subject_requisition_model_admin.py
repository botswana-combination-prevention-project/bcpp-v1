from lab_requisition.admin import BaseRequisitionModelAdmin
from bcpp_subject.models import SubjectVisit


class SubjectRequisitionModelAdmin (BaseRequisitionModelAdmin):

    visit_model = SubjectVisit
    visit_fieldname = 'subject_visit'
    dashboard_type = 'subject'
