from base_htc_model_form import BaseHtcModelForm
from bcpp_htc_subject.models import DemographicsRisk


class DemographicsRiskForm (BaseHtcModelForm):

    class Meta:
        model = DemographicsRisk
