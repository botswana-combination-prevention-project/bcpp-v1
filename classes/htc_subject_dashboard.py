from bcpp_htc.models import HtcVisit, HtcRegistration
from base_subject_dashboard import BaseSubjectDashboard


class HtcSubjectDashboard(BaseSubjectDashboard):

    def __init__(self):
        super(HtcSubjectDashboard, self).__init__()
        self.exclude_others_if_keyed_model_name = 'htcregistration'
        self._htc_registration = None
        self.context.add(
            search_name='htc_subject',
            )

    def create(self, **kwargs):
        super(HtcSubjectDashboard, self).create(**kwargs)
        self.context.add(
            htc_registration=self.get_htc_registration(),
            title='HTC Subject Dashboard',
            )

    def set_membership_form_category(self):
        self._membership_form_category = (self.get_survey().survey_slug)

    def set_htc_registration(self):
        self._htc_registration = self.get_consent()

    def get_htc_registration(self):
        if not self._htc_registration:
            self.set_htc_registration()
        return self._htc_registration

    def set_consent(self):
        self._consent = None
        if HtcRegistration.objects.filter(registered_subject=self.get_registered_subject()):
            self._consent = HtcRegistration.objects.get(registered_subject=self.get_registered_subject())

    def set_visit_model(self):
        if self.get_dashboard_type() == 'htc_subject':
            self._visit_model = HtcVisit

#     def set_requisition_model(self):
#         if self.get_dashboard_type() == 'htc_subject':
#             self._requisition_model = HtcRequisition
# 
#     def set_packing_list_model(self):
#         if self.get_dashboard_type() == 'htc_subject':
#             self._packing_list_model = HtcPackingList

