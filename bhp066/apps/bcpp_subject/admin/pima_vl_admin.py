from django.contrib import admin
from ..models import PimaVl
from ..forms import PimaVlForm
from .subject_visit_model_admin import SubjectVisitModelAdmin
from ..filters import Cd4ThreshHoldFilter

from django.contrib.auth.models import User

from edc_tracker import TrackerHelper


class PimaVlAdmin(SubjectVisitModelAdmin):

    form = PimaVlForm
    fields = (
        "subject_visit",
        'poc_vl_today',
        'poc_vl_today_other',
        'poc_today_vl_other_other',
        'pima_id',
        'cd4_value',
        'time_of_test',
        'time_of_result',
        'easy_of_use',
        'stability',
        )
    exclude = ('poc_vl_type',)
    list_filter = ('subject_visit', 'time_of_test', 'pima_id', Cd4ThreshHoldFilter,)
    list_display = ('subject_visit', 'time_of_test', 'cd4_value', 'pima_id')
    radio_fields = {
        'poc_vl_today': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        pass
        #self.valid_user(self, request.user)
        #obj.save()

    def valid_user(self, user):
        """ A list for user contacts."""
        pass
#         tracker = TrackerHelper()
#         if tracker.tracked_value < 400:
#             if not user in User.objects.filter(groups__name='field_supervisor'):
#                 raise "Access denied, you don't have permission to save/modified this model."
#         else:
#             if not user in User.objects.filter(groups__name='field_research_assistant'):
#                 raise "Access denied, you don't have permission to save/modified this model."
#         return True
admin.site.register(PimaVl, PimaVlAdmin)
