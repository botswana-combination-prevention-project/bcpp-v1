from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bcpp_subject.models import SubjectConsent, SubjectVisit, SubjectLocator
from bcpp_lab.models import SubjectRequisition


class SubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self, **kwargs):

        self.dashboard_type = 'subject'
        super(SubjectDashboard, self).__init__(**kwargs)
        self.visit_model = SubjectVisit
        self.visit_model_app_label = SubjectVisit._meta.app_label
        self.visit_model_name = SubjectVisit._meta.module_name
        self.requisition_model = SubjectRequisition
        self.subject_type = 'subject'

        self.context.add(
            visit_model_name=self.visit_model_name,
            requisition_model=SubjectRequisition,
            visit_model=self.visit_model,
            visit_model_app_label=self.visit_model_app_label,
            subject_type=self.subject_type,
            home=kwargs.get('home', 'bcpp'),
            search_name=kwargs.get('search_name', 'subject'),
            )

    def create(self, **kwargs):
        self.dashboard_identifier = kwargs.get("registered_subject").subject_identifier
        super(SubjectDashboard, self).create(**kwargs)
        subject_consent = SubjectConsent.objects.get(subject_identifier=self.get_subject_identifier())
        if self.visit_code:
            self.check_entry_status()
        subject_locator = None
        if SubjectLocator.objects.filter(subject_visit__appointment__registered_subject__subject_identifier=self.get_subject_identifier()):
            subject_locator = SubjectLocator.objects.get(subject_visit__appointment__registered_subject__subject_identifier=self.get_subject_identifier())

        self.context.add(
            subject_consent=subject_consent,
            subject_locator=subject_locator,
            locator=self.render_locator(SubjectLocator),
            local_results=self.render_labs())
