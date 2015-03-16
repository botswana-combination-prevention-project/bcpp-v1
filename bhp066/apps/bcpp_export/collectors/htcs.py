from apps.bcpp_household_member.models import HouseholdMember

from ..classes import Htc

from .base_collector import BaseCollector


class Htcs(BaseCollector):

    """Exports helper.household instances to CSV.

    For example::
        from apps.bcpp_export.collectors import Members

        members = Members()
        members.export_to_csv()
    """

    def __init__(self, export_plan=None, community=None, survey_slug=None, exception_cls=None):
        super(Htcs, self).__init__(export_plan=export_plan, community=community, exception_cls=exception_cls)
        self.survey_slug = survey_slug

    def export_to_csv(self):
        for community in self.community_list:
            print '{} **************************************'.format(community)
            filter_options = {'household_structure__household__plot__community': community}
            exclude_options = {'household_structure__household__plot__plot_identifier__endswith': '0000-00'}
            if self.survey_slug:
                filter_options.update({'household_structure__survey__survey_slug': self.survey_slug})
            household_members = HouseholdMember.objects.filter(
                **filter_options).exclude(
                **exclude_options).order_by('household_structure__household__household_identifier',
                                            'household_structure__survey__survey_slug')
            for household_member in household_members:
                htc = Htc(household_member)
                self._export(htc)
                if self.test_run:
                    break
