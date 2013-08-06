from importlib import import_module
from django.test import TestCase
from django.db.models import get_model
from bhp_base_model.models import BaseModel
from bcpp_subject import choices
from bcpp_subject import models


class ChoiceTests(TestCase):

    def test_p1(self):
        dct = {}
        for choice in [item for item in dir(choices) if not item.startswith('_')]:
            c = getattr(import_module('bcpp_subject.choices'), choice)
            for tpl in c:
                if dct.get(choice):
                    if dct.get(choice)[0] < len(tpl[0]):
                        dct.update({choice: (len(tpl[0]), tpl[0])})
                else:
                    dct.update({choice: (len(tpl[0]), tpl[0])})
        for model in  [item for item in dir(models) if not item.startswith('_')]:
            m = get_model('bcpp_subject', model.replace('_', ''))
            if m:
                if issubclass(m, BaseModel):
                    for field in m._meta.fields:
                        for choice in [item for item in dir(choices) if not item.startswith('_')]:
                            c = getattr(import_module('bcpp_subject.choices'), choice)
                            if field.choices == c:
                                self.assertTrue(dct.get(choice)[0] <= field.max_length, msg='{0}.{1} max_length={2} but {3} max length is {4} '.format(m._meta.object_name, field.name, field.max_length, choice, dct.get(choice)[0]))
