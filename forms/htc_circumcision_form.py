from base_htc_model_form import BaseHtcModelForm
from bcpp_htc_subject.models import HtcCircumcision


class HtcCircumcisionForm (BaseHtcModelForm):

    class Meta:
        model = HtcCircumcision
