from base_off_study import BaseOffStudy


class TestOffStudy(BaseOffStudy):

    def get_requires_consent(self):
        return False

    def get_visit_model_app(self):
        return 'bhp_visit_tracking'

    class Meta:
        app_label = 'bhp_off_study'
