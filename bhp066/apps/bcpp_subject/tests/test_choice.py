from importlib import import_module

from django.conf import settings
from django.db.models import get_model
from django.test import TestCase
from django.utils import translation

from edc_base.model.models import BaseModel

from .. import choices
from .. import models


class TestChoice(TestCase):
    """Tests that the choices are correctly formated."""
    def test_p1(self):
        """Assert choices left item fits in its model.field."""
        MAX_LENGTH = 0
        TEXT = 1
        found = False
        # print 'check choices tuples fit in their fields (in English)'
        for language in settings.LANGUAGES:
            if language == ('en', 'English'):
                found = True
                translator = translation.trans_real.translation(language[0])
                dct = {}
                for choice in [item for item in dir(choices) if not item.startswith('_')]:
                    c = getattr(import_module('bhp066.apps.bcpp_subject.choices'), choice)
                    for tpl in c:
                        if dct.get(choice):
                            text = translator.ugettext(tpl[0])
                            # print (text, tpl[0])
                            if dct.get(choice)[MAX_LENGTH] < len(text):
                                dct.update({choice: (len(text), text)})
                        else:
                            dct.update({choice: (len(tpl[0]), tpl[0])})
                for model in [item for item in dir(models) if not item.startswith('_')]:
                    m = get_model('bcpp_subject', model.replace('_', ''))
                    if m:
                        if issubclass(m, BaseModel):
                            for field in m._meta.fields:
                                for choice in [item for item in dir(choices) if not item.startswith('_')]:
                                    c = getattr(import_module('bhp066.apps.bcpp_subject.choices'), choice)
                                    if field.choices == c:
                                        self.assertTrue(dct.get(choice)[MAX_LENGTH] <= field.max_length, msg='{0}.{1} max_length={2} but {3} max length is {4} '.format(m._meta.object_name, field.name, field.max_length, choice, dct.get(choice)[TEXT]))
        if not found:
            raise TypeError('Language not found!')
