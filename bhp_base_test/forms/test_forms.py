from bhp_base_form.forms import BaseModelForm
from bhp_base_test.models import TestModel, TestSubjectUuidModel


class TestSubjectUuidModelForm (BaseModelForm):

    class Meta:
        model = TestSubjectUuidModel


class TestModelForm (BaseModelForm):

    class Meta:
        model = TestModel
