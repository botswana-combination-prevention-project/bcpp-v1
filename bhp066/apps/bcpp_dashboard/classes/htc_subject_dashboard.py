from apps.bcpp_htc_subject.models import HtcSubjectVisit, HtcSubjectConsent, HtcSubjectLocator
from base_subject_dashboard import BaseSubjectDashboard


class HtcSubjectDashboard(BaseSubjectDashboard):

    view = 'htc_subject_dashboard'
    dashboard_name = 'HTC Subject Dashboard'

    def __init__(self, **kwargs):
        self.dashboard_type = 'htc_subject'
        kwargs.update({'dashboard_models': {'htc_subject_consent': HtcSubjectConsent}})
        super(HtcSubjectDashboard, self).__init__(**kwargs)

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['htc_subject']

    def get_locator_model(self):
        return HtcSubjectLocator

    def set_consent(self):
        self._consent = None
        if HtcSubjectConsent.objects.filter(registered_subject=self.get_registered_subject()):
            self._consent = HtcSubjectConsent.objects.get(registered_subject=self.get_registered_subject())

    def get_visit_model(self):
        return HtcSubjectVisit
