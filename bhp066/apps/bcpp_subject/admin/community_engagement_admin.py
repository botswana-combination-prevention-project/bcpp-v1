from django.contrib import admin

# from edc.apps.admin_supplemental_fields.admin import SupplementalModelAdminMixin
# from edc.apps.admin_supplemental_fields.classes import SupplementalFields

from ..forms import CommunityEngagementForm
from ..models import CommunityEngagement

from .subject_visit_model_admin import SubjectVisitModelAdmin


class CommunityEngagementAdmin(SubjectVisitModelAdmin):

    form = CommunityEngagementForm
#     supplemental_fields = SupplementalFields(
#         ('community_engagement',
#         'vote_engagement',
#         'problems_engagement',
#         'problems_engagement_other',
#         'solve_engagement',), p=0.09, group='CE', grouping_field='subject_visit')
    fields = (
        "subject_visit",
        'community_engagement',
        'vote_engagement',
        'problems_engagement',
        'problems_engagement_other',
        'solve_engagement',)
    radio_fields = {
        "community_engagement": admin.VERTICAL,
        "vote_engagement": admin.VERTICAL,
        "solve_engagement": admin.VERTICAL, }
    filter_horizontal = ('problems_engagement',)
admin.site.register(CommunityEngagement, CommunityEngagementAdmin)
