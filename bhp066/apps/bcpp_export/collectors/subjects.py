from apps.bcpp_subject.models import SubjectConsent

from ..classes import Subject

from .base_collector import BaseCollector


class Subjects(BaseCollector):

    """Exports helper.household instances to CSV.

    For example::
        from apps.bcpp_export.collectors import Subjects

        subjects = Subjects()
        subjects.export_to_csv()
    """

    def __init__(self, export_plan=None, community=None, survey_slug=None, exception_cls=None):
        super(Subjects, self).__init__(export_plan=export_plan, community=community, exception_cls=exception_cls)
        self.survey_slug = survey_slug

    def export_to_csv(self):
        for community in self.community_list:
            print '{} **************************************'.format(community)
            filter_options = {'household_member__household_structure__household__plot__community': community}
            exclude_options = {'household_member__household_structure__household__plot__plot_identifier__endswith': '0000-00'}
            if self.survey_slug:
                filter_options.update({'household_member__household_structure__survey__survey_slug': self.survey_slug})
            subject_consents = SubjectConsent.objects.filter(
                **filter_options).exclude(
                **exclude_options).order_by('registered_subject__subject_identifier')
            for subject_consent in subject_consents:
                subject = Subject(subject_consent.household_member)
                self._export(subject)
                if self.test_run:
                    break
