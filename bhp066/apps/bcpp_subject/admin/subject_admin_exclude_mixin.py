from edc_admin_exclude.admin import AdminExcludeFieldsMixin

from ..constants import BASELINE, ANNUAL
from ..models import SubjectVisit


class SubjectAdminExcludeMixin(AdminExcludeFieldsMixin):

    visit_model = SubjectVisit
    visit_attr = 'subject_visit'
    visit_codes = {BASELINE: ['T0'], ANNUAL: ['T1', 'T2', 'T3']}
