import random
from bhp_supplemental_fields.models import Excluded
from base import Base


class ConditionalFields(Base):

    def __init__(self, conditional_fields, **kwargs):
        super(ConditionalFields, self).__init__(conditional_fields, 'conditional_fields')

    def _choice(self, exclude_fields):
        if random.choice(self._get_p_as_sequence()):  # either 0 or 1
            exclude_fields = tuple(self._get_optional_fields())
        return exclude_fields

    def _stored_choice(self, exclude_fields, obj):
        if obj:
            raise AttributeError('Attribute \'obj\' cannot be None.')
        if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk).exists():
            exclude_fields = self._get_optional_fields()
        return exclude_fields
