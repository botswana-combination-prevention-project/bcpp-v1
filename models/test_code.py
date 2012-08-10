from lab_test_code.models import BaseTestCode


class TestCode(BaseTestCode):

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ["name"]
        app_label = 'lab_clinic_api'
