from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import MedicalDiagnoses
from bcpp_subject.forms import MedicalDiagnosesForm



class MedicalDiagnosesAdmin(SubjectVisitModelAdmin):

    form = MedicalDiagnosesForm
    fields = (
        "subject_visit",
       'diagnoses',
       'heart_attack_record',
       'cancer_record',
       'sti_record',
       'tb_record',)
    radio_fields = {
        "heart_attack_record": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "sti_record": admin.VERTICAL,
        "tb_record": admin.VERTICAL, }
    filter_horizontal = ('diagnoses',)
    required_instructions = ("Read to Participant: I am now going to ask you"
                             "some questions about major illnesses that you may"
                             "have had in the past 12 months. Sometimes people"
                             "call different sicknesses by different names."
                             "If you do not understand what I mean, please ask."
                             "Also, please remember that your answers will be"
                             "kept confidential.")
admin.site.register(MedicalDiagnoses, MedicalDiagnosesAdmin)
