from edc.subject.off_study.mixins import OffStudyMixin
from .clinic_off_study import ClinicOffStudy


class ClinicOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        return ClinicOffStudy
