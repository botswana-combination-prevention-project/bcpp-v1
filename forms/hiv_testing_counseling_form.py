from bcpp_subject.forms import BaseSubjectModelForm
from bcpp_htc.models import HivTestingCounseling


class HivTestingCounselingForm (BaseSubjectModelForm):

    class Meta:
        model = HivTestingCounseling