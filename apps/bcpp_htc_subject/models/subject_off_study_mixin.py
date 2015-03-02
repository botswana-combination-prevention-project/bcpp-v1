from edc.subject.off_study.mixins import OffStudyMixin
from .htc_subject_off_study import HtcSubjectOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return HtcSubjectOffStudy
