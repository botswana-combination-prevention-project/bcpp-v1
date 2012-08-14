from lab_test_code.models import BaseTestCodeGroup


class TestCodeGroup(BaseTestCodeGroup):

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['code', ]
