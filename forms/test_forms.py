from bhp_consent.models import TestSubjectUuidModel
from bhp_consent.forms import BaseConsentedModelForm


class TestSubjectUuidModelForm (BaseConsentedModelForm):

    class Meta:
        model = TestSubjectUuidModel
