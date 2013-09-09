from bhp_off_study.mixins import OffStudyMixin
from test_base_off_study import TestBaseOffStudy


class TestOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return TestBaseOffStudy
