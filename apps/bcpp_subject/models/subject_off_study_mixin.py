from edc.subject.off_study.mixins import OffStudyMixin

from .subject_off_study import SubjectOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return SubjectOffStudy
