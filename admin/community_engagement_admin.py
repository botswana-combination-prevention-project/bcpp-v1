from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import CommunityEngagement
from bcpp_subject.forms import CommunityEngagementForm


class CommunityEngagementAdmin(SubjectVisitModelAdmin):

    form = CommunityEngagementForm
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