from django.contrib import admin
from django.utils.encoding import force_unicode
from django.db.models import get_model
from datetime import datetime

from edc_quota import Override


from .subject_visit_model_admin import SubjectVisitModelAdmin
from ..models import PimaVl
from ..forms import PimaVlForm
from ..filters import Cd4ThreshHoldFilter


class PimaVlAdmin(SubjectVisitModelAdmin):

    form = PimaVlForm
    fields = (
        "subject_visit",
        'poc_vl_today',
        'poc_vl_today_other',
        'poc_today_vl_other_other',
        'pima_id',
        'poc_vl_value',
        'time_of_test',
        'time_of_result',
        'easy_of_use',
        'stability',
        'confirmation_code',
        )
    exclude = ('poc_vl_type',)
    list_filter = ('subject_visit', 'time_of_test', 'pima_id', Cd4ThreshHoldFilter,)
    list_display = ('subject_visit', 'time_of_test', 'poc_vl_value', 'pima_id')
    radio_fields = {
        'poc_vl_today': admin.VERTICAL,
        'poc_vl_today_other': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}

    @property
    def client_key_instructions(self):
        return  'You have reached quota limit. Send client code: <span style="color:red;">{0}</span> to CBS for confirmation key to increase quota limit. otherwise ignore the key.'.\
            format(Override().code) if PimaVl().quota_reached else ''

    @property
    def required_instructions(self):
        required_instructions = (
            'Required questions are in bold. '
            'When all required data has been entered click SAVE to return to the dashboard '
            'or SAVE NEXT to go to the next form (if available). Additional questions may be required'
            'or may need to be corrected when you attempt to save.<br><strong>{}</strong>'.format(self.client_key_instructions))
        return required_instructions

admin.site.register(PimaVl, PimaVlAdmin)
