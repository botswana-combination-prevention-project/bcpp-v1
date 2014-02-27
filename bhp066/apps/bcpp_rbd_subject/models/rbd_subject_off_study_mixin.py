from apps.bcpp_subject.models import SubjectOffStudyMixin
from .rbd_off_study import RBDSubjectOffStudy


class RBDSubjectOffStudyMixin(SubjectOffStudyMixin):

    def get_off_study_cls(self):
        return RBDSubjectOffStudy
