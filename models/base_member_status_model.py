from django.db.models import get_models, get_app
from bhp_appointment_helper.models import BaseAppointmentMixin
from base_registered_household_structure_member_model import BaseRegisteredHouseholdStructureMemberModel


class BaseMemberStatusModel(BaseRegisteredHouseholdStructureMemberModel, BaseAppointmentMixin):

    def __unicode__(self):
        return '{0} {1}'.format(self.member_status_string().lower(), self.get_report_datetime().strftime('%Y-%m-%d'))

    def get_report_datetime(self):
        return self.report_datetime

    def member_status_string(self):
        """Returns a the value for updating household_structure_member.member_status.

        For example: CONSENTED, ABSENT, REFUSED"""
        return None

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'household'), 'household_structure_member__household_structure__household')

    def post_save_update_hsm_status(self, using=None):
        """Updates the hsm member_status."""
        hsm = self.household_structure_member
        if not hsm.member_status == 'CONSENTED':
            if self.member_status_string() == 'CONSENTED':
                # consent overwrites everything else
                hsm.member_status = self.member_status_string()
            else:
                # among these model classes look for an instance with the most recent report_datetime
                # and set hsm member_status to the status from that instance (member_status_string())
                # or just use self.member_status_string()
                max_report_datetime = self.report_datetime
                selected_instance = self
                app = get_app(self._meta.app_label)
                status_models = []
                for cls in get_models(app):
                    if 'member_status_string' in dir(cls) and not cls == self.__class__:
                        status_models.append(cls)
                for status_model in status_models:
                    if status_model.objects.using(using).filter(household_structure_member=self.household_structure_member).exists():
                        instance = status_model.objects.using(using).get(household_structure_member=self.household_structure_member)
                        if instance.report_datetime > max_report_datetime:
                            max_report_datetime = instance.report_datetime
                            selected_instance = instance
                hsm.member_status = selected_instance.member_status_string()
            hsm.save(using=using)

    class Meta:
        abstract = True
