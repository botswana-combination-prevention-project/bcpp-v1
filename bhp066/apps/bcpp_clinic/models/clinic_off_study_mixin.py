from .clinic_off_study import ClinicOffStudy

from edc.subject.off_study.mixins import OffStudyMixin


class ClinicOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return ClinicOffStudy

    class Meta:
        abstract = True
