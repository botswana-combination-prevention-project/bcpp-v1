from bhp_consent.forms import BaseConsentedModelForm
from bhp_base_test.models import TestSubjectUuidModel


class TestSubjectUuidModelForm (BaseConsentedModelForm):

    class Meta:
        model = TestSubjectUuidModel
