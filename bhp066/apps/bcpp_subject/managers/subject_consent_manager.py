from django.conf import settings

from edc.map.classes import site_mappers
from edc.subject.subject.managers import BaseSubjectManager


class SubjectConsentManager(BaseSubjectManager):

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            return super(SubjectConsentManager, self).get_queryset().filter(community=community)
        return super(SubjectConsentManager, self).get_queryset()
