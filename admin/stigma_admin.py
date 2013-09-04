from django.contrib import admin
from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import Stigma, StigmaOpinion, PositiveParticipant
from bcpp_subject.forms import StigmaForm, StigmaOpinionForm, PositiveParticipantForm


"""Stigma [ST]: 10% in pretest. In BHS, it differs according to reported HIV status:
    9% on ST1-ST12 for reported negative; 18% on ST1-ST19 for reported positive."""

class StigmaAdmin(SubjectVisitModelAdmin):

    form = StigmaForm
    supplemental_fields = SupplementalFields(
        ('anticipate_stigma',
        'enacted_shame_stigma',
        'saliva_stigma',
        'teacher_stigma',
        'children_stigma'),p=0.09, group='ST')
    fields = (
        "subject_visit",
        'anticipate_stigma',
        'enacted_shame_stigma',
        'saliva_stigma',
        'teacher_stigma',
        'children_stigma',)
    radio_fields = {
        "anticipate_stigma": admin.VERTICAL,
        "enacted_shame_stigma": admin.VERTICAL,
        "saliva_stigma": admin.VERTICAL,
        "teacher_stigma": admin.VERTICAL,
        "children_stigma": admin.VERTICAL, }
    instructions = [("Interviewer Note: The following supplemental "
                             "questions are only asked for respondents NOT known"
                             " to have HIV. SKIP for respondents with known HIV infection."
                             " Read to Participant: Different people feel differently about"
                             " people living with HIV. I am going to ask you about issues"
                             " relevant to HIV and AIDS and also people living with HIV."
                             " Some of the questions during the interview will ask for your"
                             " opinion on how you think people living with HIV are treated."
                             " To start, when thinking about yourself, please tell me how "
                             " strongly you agree or disagree with the following statements.")]
admin.site.register(Stigma, StigmaAdmin)


class StigmaOpinionAdmin(SubjectVisitModelAdmin):

    form = StigmaOpinionForm
    supplemental_fields = SupplementalFields(
        ('test_community_stigma',
        'gossip_community_stigma',
        'respect_community_stigma',
        'enacted_verbal_stigma',
        'enacted_phyical_stigma',
        'enacted_family_stigma',
        'fear_stigma'),p=0.09, group='ST')
    fields = (
        "subject_visit",
        'test_community_stigma',
        'gossip_community_stigma',
        'respect_community_stigma',
        'enacted_verbal_stigma',
        'enacted_phyical_stigma',
        'enacted_family_stigma',
        'fear_stigma',)
    radio_fields = {
        "test_community_stigma": admin.VERTICAL,
        "gossip_community_stigma": admin.VERTICAL,
        "respect_community_stigma": admin.VERTICAL,
        "enacted_verbal_stigma": admin.VERTICAL,
        "enacted_phyical_stigma": admin.VERTICAL,
        "enacted_family_stigma": admin.VERTICAL,
        "fear_stigma": admin.VERTICAL, }
    instructions = [("Read to Participant: Using your own opinions and"
                             " thinking about this community, please tell me how"
                             " strongly you agree or disagree with the following"
                             " statements.")]
admin.site.register(StigmaOpinion, StigmaOpinionAdmin)


class PositiveParticipantAdmin(SubjectVisitModelAdmin):

    form = PositiveParticipantForm
    supplemental_fields = SupplementalFields(
        ('internalize_stigma',
        'internalized_stigma',
        'friend_stigma',
        'family_stigma',
        'enacted_talk_stigma',
        'enacted_respect_stigma',
        'enacted_jobs_tigma'),p=0.18, group='ST')
    fields = (
        "subject_visit",
        'internalize_stigma',
        'internalized_stigma',
        'friend_stigma',
        'family_stigma',
        'enacted_talk_stigma',
        'enacted_respect_stigma',
        'enacted_jobs_tigma',)
    radio_fields = {
        "internalize_stigma": admin.VERTICAL,
        "internalized_stigma": admin.VERTICAL,
        "friend_stigma": admin.VERTICAL,
        "family_stigma": admin.VERTICAL,
        "enacted_talk_stigma": admin.VERTICAL,
        "enacted_respect_stigma": admin.VERTICAL,
        "enacted_jobs_tigma": admin.VERTICAL, }
    instructions = [("Interviewer Note: The following supplemental questions"
                             " are only asked for respondents with known HIV infection."
                             " SKIP for respondents without known HIV infection. "
                             " Read to Participant: You let us know earlier that you"
                             " are HIV positive. I would now like to ask you a few"
                             " questions about your experiences living with HIV."
                             " Please remember this interview and your responses"
                             " are private and confidential.In this section,"
                             " I'm going to read you statements"
                             "  about how you may feel about yourself and your "
                             " HIV/AIDS infection. I would like you to tell me"
                             " if you strongly agree, agree, disagree or strongly"
                             " disagree with each statement?")]
admin.site.register(PositiveParticipant, PositiveParticipantAdmin)
