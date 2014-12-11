from django.contrib import admin
from django.utils.translation import ugettext as _

# from edc.apps.admin_supplemental_fields.admin import SupplementalModelAdminMixin
# from edc.apps.admin_supplemental_fields.classes import SupplementalFields

from ..forms import PositiveParticipantForm
from ..models import PositiveParticipant

from .subject_visit_model_admin import SubjectVisitModelAdmin


class PositiveParticipantAdmin(SubjectVisitModelAdmin):

    form = PositiveParticipantForm
#     supplemental_fields = SupplementalFields(
#         ('internalize_stigma',
#          'internalized_stigma',
#          'friend_stigma',
#          'family_stigma',
#          'enacted_talk_stigma',
#          'enacted_respect_stigma',
#          'enacted_jobs_tigma'), p=0.18, group='PP', grouping_field='subject_visit')
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
    instructions = [(
        "<h5>Interviewer Note</h5> The following supplemental questions"
        " are only asked for respondents with known HIV infection."
        " SKIP for respondents without known HIV infection. "),
        _(" Read to Participant: You let us know earlier that you"
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
