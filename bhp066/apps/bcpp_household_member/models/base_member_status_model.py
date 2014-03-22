from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


class BaseMemberStatusModel(BaseRegisteredHouseholdMemberModel):

    def __unicode__(self):
        return '{0} {1}'.format(self.household_member.member_status.lower(), self.get_report_datetime().strftime('%Y-%m-%d'))

    def get_report_datetime(self):
        return self.report_datetime

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

    class Meta:
        abstract = True
