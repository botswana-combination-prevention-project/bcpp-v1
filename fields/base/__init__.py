from django.db.models import CharField as CField
from django.db.models import DateField as DField
from django.db.models import DateTimeField as DTField
from django.db.models import IntegerField as IField


class CharField(CField):
    pass
#     def __init__(self, *args, **kwargs):
#         self.randomize = kwargs.get('randomize', None)
#         super(CharField, self).__init__(*args, **kwargs)
#     def contribute_to_class(self, cls, name):
#         #assert not cls._meta.has_randomizer, \
#         #       "A model can't have more than one Randomizer."
#         super(CharField, self).contribute_to_class(cls, name)
#         if 'randomize' in dir(cls):
#             cls._meta.randomizer.append(cls.)


class DateField(DField):
    pass


class DateTimeField(DTField):
    pass


class IntegerField(IField):
    pass
