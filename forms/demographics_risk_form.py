from bcpp_htc_subject.models import DemographicsRisk
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class DemographicsRiskForm (BaseHtcScheduledModelForm):

    class Meta:
        model = DemographicsRisk
