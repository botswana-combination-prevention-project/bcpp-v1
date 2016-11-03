from django.contrib import admin

from ..constants import ANNUAL
from ..forms import DemographicsForm
from ..models import Demographics

from .subject_admin_exclude_mixin import SubjectAdminExcludeMixin
from .subject_visit_model_admin import SubjectVisitModelAdmin


class DemographicsAdmin(SubjectAdminExcludeMixin, SubjectVisitModelAdmin):

    form = DemographicsForm

    fields = [
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'ethnic_other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with']

    custom_exclude = {
        ANNUAL:
            ['religion', 'religion_other', 'ethnic', 'ethnic_other']
    }

    radio_fields = {
        "marital_status": admin.VERTICAL, }

    filter_horizontal = ('live_with', 'religion', 'ethnic')

admin.site.register(Demographics, DemographicsAdmin)
