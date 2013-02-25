from base_off_study import BaseOffStudy


class TestOffStudy(BaseOffStudy):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_off_study'
