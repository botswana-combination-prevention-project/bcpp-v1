from base_visit_tracking import BaseVisitTracking


class TestSubjectVisit(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_visit_tracking'
