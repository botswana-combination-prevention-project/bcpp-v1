from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import MedicalDiagnoses
from ..forms import MedicalDiagnosesForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class MedicalDiagnosesAdmin(SubjectVisitModelAdmin):

    form = MedicalDiagnosesForm
    fields = (
        'subject_visit',
        'diagnoses',
        'heart_attack_record',
        'cancer_record',
        'tb_record',
    )
    radio_fields = {
        "heart_attack_record": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "tb_record": admin.VERTICAL, }
    filter_horizontal = ('diagnoses',)
    baseline_instructions = [_(
        "<h5>Read to Participant</h5> I am now going to ask you"
        " some questions about major illnesses that you may"
        " have had in the past 12 months. Sometimes people"
        " call different sicknesses by different names."
        " If you do not understand what I mean, please ask."
        " Also, please remember that your answers will be"
        " kept confidential.")]

    annual_instructions = [
        _("<h5>Read to Participant</h5> I am now going to ask you"
          " some questions about major illnesses that you may"
          " have had since we spoke with you at our last visit. Sometimes people"
          " call different sicknesses by different names."
          " If you do not understand what I mean, please ask."
          " Also, please remember that your answers will be"
          " kept confidential."),
    ]
admin.site.register(MedicalDiagnoses, MedicalDiagnosesAdmin)
