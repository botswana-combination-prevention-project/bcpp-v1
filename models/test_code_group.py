from base_test_code_group import BaseTestCodeGroup


class TestCodeGroup(BaseTestCodeGroup):

    class Meta:
        app_label = 'lab_test_code'
        db_table = 'bhp_lab_test_code_testcodegroup'
        ordering = ['code', ]
