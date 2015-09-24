from edc.subject.off_study.mixins import OffStudyMixin
from .htc_subject_off_study import HtcSubjectOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL =  HtcSubjectOffStudy
