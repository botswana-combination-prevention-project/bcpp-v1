from django.contrib import admin

from ..forms import StigmaOpinionForm
from ..models import StigmaOpinion

from .subject_visit_model_admin import SubjectVisitModelAdmin


class StigmaOpinionAdmin(SubjectVisitModelAdmin):

    form = StigmaOpinionForm
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
    instructions = [
        ("<h5>Read to Participant</h5>Using your own opinions and"
         " thinking about this community, please tell me how"
         " strongly you agree or disagree with the following"
         " statements.")]
admin.site.register(StigmaOpinion, StigmaOpinionAdmin)
