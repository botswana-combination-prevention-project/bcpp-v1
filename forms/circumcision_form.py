from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import Circumcision


class CircumcisionForm (BaseHtcModelForm):

    class Meta:
        model = Circumcision
