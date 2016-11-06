from edc_offstudy.model_mixins import OffStudyMixin

from .subject_off_study import SubjectOffStudy


class SubjectOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = SubjectOffStudy

    class Meta:
        abstract = True
