from lab_test_code.models import BaseTestCode


class TestCode(BaseTestCode):

    class Meta:
        ordering = ["name"]
        app_label = 'lab_clinic_api'
