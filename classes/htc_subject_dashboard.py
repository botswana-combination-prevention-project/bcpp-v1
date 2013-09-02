from bcpp_htc.models import HtcVisit, HtcRegistration, HtcLocator
from base_subject_dashboard import BaseSubjectDashboard


class HtcSubjectDashboard(BaseSubjectDashboard):

    view = 'htc_subject_dashboard'
    dashboard_name = 'HTC Subject Dashboard'

    def __init__(self, **kwargs):
        self.dashboard_type = 'htc_subject'
        kwargs.update({'dashboard_models': {'htc_registration': HtcRegistration}})
        super(HtcSubjectDashboard, self).__init__(**kwargs)

    def add_to_context(self):
        super(BaseSubjectDashboard, self).add_to_context()
        self.context.add(htc_registration=self.get_htc_registration())

#     def set_membership_form_category(self):
#         self._membership_form_category = 'htc_subject'

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['htc_subject']

    def set_htc_registration(self):
        self._htc_registration = self.get_consent()

    def get_htc_registration(self):
        if not self._htc_registration:
            self.set_htc_registration()
        return self._htc_registration

    def get_locator_model(self):
        return HtcLocator

    def set_consent(self):
        self._consent = None
        if HtcRegistration.objects.filter(registered_subject=self.get_registered_subject()):
            self._consent = HtcRegistration.objects.get(registered_subject=self.get_registered_subject())

    def get_visit_model(self):
        return HtcVisit
