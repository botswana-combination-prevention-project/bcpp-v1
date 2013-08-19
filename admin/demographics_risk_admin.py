from django.contrib import admin
from bcpp_subject.admin.subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_htc.models import DemographicsRisk
from bcpp_htc.forms import DemographicsRiskForm


class DemographicsRiskAdmin(SubjectVisitModelAdmin):

    form = DemographicsRiskForm

    fields = (
        "subject_visit",
        "report_datetime",
        "education",
        "employment",
        "marital_status",
        "alcohol_intake",
    )
    radio_fields = {
        "education": admin.VERTICAL,
        "employment": admin.VERTICAL,
        "marital_status": admin.VERTICAL,
        "alcohol_intake": admin.VERTICAL}
    instructions = [("Read to Participant: Now I will ask some questions about"
                     " sex and sex partners.  Some of these questions may make"
                     " you uncomfortable; however, please remember that your"
                     " answers are confidential and it is really important for"
                     " us to get the most honest answer you can give us."
                     "  In this set of questions, when I say sex, I mean"
                     " vaginal or anal sex.  I do not mean oral sex, kissing,"
                     " or touching with hands.  When I say a partner, I mean"
                     " anyone you might have had sex with.  Partners can be"
                     " your husband, wife or wives, girlfriends, boyfriends,"
                     " friends, casual partners, prostitutes, or someone you"
                     " may have met at a bar, or at a wedding or other special"
                     " events, etc.")]

admin.site.register(DemographicsRisk, DemographicsRiskAdmin)
