from django.contrib import admin

#from edc.apps.admin_supplemental_fields.admin import SupplementalModelAdminMixin
#from edc.apps.admin_supplemental_fields.classes import SupplementalFields

from ..forms import HivUntestedForm
from ..models import HivUntested

from .subject_visit_model_admin import SubjectVisitModelAdmin


# HIV testing and history [HT]: 10% in pretest, 9% in BHS and all follow-up
class HivUntestedAdmin(SubjectVisitModelAdmin):

    form = HivUntestedForm
#     supplemental_fields = SupplementalFields(
#         ('why_no_hiv_test',
#          'hiv_pills',
#          'arvs_hiv_test'), p=0.09, group='HT', grouping_field='subject_visit')
    fields = (
        "subject_visit",
        'why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "why_no_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
admin.site.register(HivUntested, HivUntestedAdmin)
