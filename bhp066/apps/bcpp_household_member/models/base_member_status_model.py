from django.db.models import get_models, get_app

from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


class BaseMemberStatusModel(BaseRegisteredHouseholdMemberModel):

    def __unicode__(self):
        return '{0} {1}'.format(self.member_status_string().lower(), self.get_report_datetime().strftime('%Y-%m-%d'))

    def get_report_datetime(self):
        return self.report_datetime

    def member_status_string(self):
        """Returns a the value for updating household_member.member_status.

        For example: CONSENTED, ABSENT, REFUSED"""
        return None

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

    def post_save_update_hm_status(self, using=None):
        """Updates the hm member_status."""
        hm = self.household_member
        if not hm.member_status_full == 'CONSENTED':
            if self.member_status_string() == 'CONSENTED':
                # consent overwrites everything else
                hm.member_status_full = self.member_status_string()
            else:
                # among these model classes look for an instance with the most recent report_datetime
                # and set hm member_status to the status from that instance (member_status_string())
                # or just use self.member_status_string()
                max_report_datetime = self.report_datetime
                selected_instance = self
                app = get_app(self._meta.app_label)
                status_models = []
                for cls in get_models(app):
                    if 'member_status_string' in dir(cls) and not cls == self.__class__:
                        status_models.append(cls)
                for status_model in status_models:
                    if status_model.objects.using(using).filter(household_member=self.household_member).exists():
                        instance = status_model.objects.using(using).get(household_member=self.household_member)
                        if instance.report_datetime > max_report_datetime:
                            max_report_datetime = instance.report_datetime
                            selected_instance = instance
                hm.member_status_full = selected_instance.member_status_string()
            hm.save(using=using)

    class Meta:
        abstract = True
