from bhp_visit_tracking.models import BaseVisitTracking


class TestVisit(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_base_test'