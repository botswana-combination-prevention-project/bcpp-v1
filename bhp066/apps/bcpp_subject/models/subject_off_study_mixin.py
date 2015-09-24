from edc.subject.off_study.mixins import OffStudyMixin

from .subject_off_study import SubjectOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = SubjectOffStudy
