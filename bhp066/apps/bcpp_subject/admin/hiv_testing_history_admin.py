from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import HivTestingHistory
from ..forms import HivTestingHistoryForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivTestingHistoryAdmin(SubjectVisitModelAdmin):

    form = HivTestingHistoryForm

    fields = (
        "subject_visit",
        'has_tested',
        "when_hiv_test",
        'has_record',
        'verbal_hiv_result',
        'other_record',)

    radio_fields = {
        "has_tested": admin.VERTICAL,
        "when_hiv_test": admin.VERTICAL,
        "has_record": admin.VERTICAL,
        "verbal_hiv_result": admin.VERTICAL,
        'other_record': admin.VERTICAL}

    instructions = [("Do not include documentation of ART/PMTCT/CD4 here; "
                    "only include actual HIV test results"),
                    _("Read to Participant: Many people have had a test"
                              " to see if they have HIV. I am going to ask you"
                              " about whether you have been tested for HIV and"
                              " whether you received the results. Please"
                              " remember that all of your answers are"
                              " confidential.")]
admin.site.register(HivTestingHistory, HivTestingHistoryAdmin)
