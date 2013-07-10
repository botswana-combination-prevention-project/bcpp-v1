import random
from bhp_supplemental_fields.models import Excluded
from base import Base


class SupplementalFields(Base):
    """ Excludes fields on the fly based on a given probability.

        * p is the probability the field will appear on the form; that is, will NOT be excluded from the fields attribute tuple
        * Fields are removed from the fields attribute tuple of an admin class.
        * Excluded fields are added to the form._meta.exclude tuple so that it operates correctly with the :func:clean method.
        * if the forms Meta class exclude attribute already specifies fields to exclude, an error will occur.

        For example::
            # If p=0.1, the supplemental fields will appear 100/1000 times the admin add form is shown.
            from bhp_base_admin.classes import SupplementalFields

            class MyModelAdmin(model.ModelAdmin):
                form = MyForm
                supplemental_fields = SupplementalFields(('regular_sex', 'having_sex', 'having_sex_reg', ), p=0.9)
                fields = ('field0', 'field1', 'regular_sex', 'having_sex', 'having_sex_reg')
                ...
    """

    def __init__(self, supplemental_fields, p, **kwargs):
        super(SupplementalFields, self).__init__(supplemental_fields, 'supplemental_fields')
        if not p < 1:
            raise AttributeError('Probability \'p\' must be less than 1. Got {0}.'.format(p))
        if len(str(p)) > 5:
            raise AttributeError('Probability \'p\' many not have more than 3 decimal places. Got {0}.'.format(p))
        self._p = p

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
