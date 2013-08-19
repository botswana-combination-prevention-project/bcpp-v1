from bcpp_subject.forms import BaseSubjectModelForm
from bcpp_htc.models import DemographicsRisk


class DemographicsRiskForm (BaseSubjectModelForm):

    class Meta:
        model = DemographicsRisk
