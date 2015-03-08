from edc.export.helpers import ExportObjectHelper
from apps.bcpp_household_member.models import HouseholdMember

from ..helpers import Subject

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
            options = {'household_structure__household__plot__community': community}
            if self.survey_slug:
                options.update({'household_structure__survey__survey_slug': self.survey_slug})
            household_members = HouseholdMember.objects.filter(
                **options).order_by('household_structure__household__household_identifier')
            for household_member in household_members:
                subject = Subject(household_member)
                self._export(subject)
                if self.test_run:
                    break
