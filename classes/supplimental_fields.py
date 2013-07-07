import copy
import random
from bhp_supplimental_fields.models import Excluded


class SupplimentalFields(object):
    """ Removes fields based on a given probability on the fly from the fields attribute of an admin class.

        If p=0.9, the supplimental fields will appear 9/10 times the admin add form is shown.

        For example::
            from bhp_base_admin.classes import SupplimentalFields

            class MyModelAdmin(model.ModelAdmin):
                form = MyForm
                supplimental_fields = SupplimentalFields(('regular_sex', 'having_sex', 'having_sex_reg', ), p=0.9)
                fields = ('field0', 'field1', 'regular_sex', 'having_sex', 'having_sex_reg')
                ...
    """

    def __init__(self, supplimental_fields, p):
        # check parameters
        if not isinstance(supplimental_fields, tuple):
            AttributeError('Attribute \'supplimental_fields\' must be a tuple of field names. Got {0}'.format(supplimental_fields))
        self.supplimental_fields = supplimental_fields
        if not p < 1:
            raise AttributeError('Probability \'p\' must be less than 1. Got {0}.'.format(p))
        if len(str(p)) > 5:
            raise AttributeError('Probability \'p\' many not have more than 3 decimal places. Got {0}.'.format(p))
        # a p of .9 means the fields will NOT be removed 9/10 times
        # convert p to a list of 0s and 1s where 1 means the fields are removed from the list
        # the sequence always has 1000 elements to allow for 3 decimal places in p
        self.p_as_sequence = ([0] * int(1000 * p)) + ([1] * int(1000 - (1000 * p)))
        self.checked_fields = False
        self.removed = {}
        self.fields = None

    def update_fields(self, fields, model, obj=None):
        # if updating for the first time, confirm all supplimental_fields exist in fields
        if not self.checked_fields:
            # check all supplimental_fields are in fields
            for supplimental_field in self.supplimental_fields:
                if supplimental_field not in fields:
                    raise AttributeError('Supplimental field \'{0}\' must be listed in fields.'.format(supplimental_field))
            # check supplimental_fields are nullable and editable
            for fld in model._meta.fields:
                if fld.name in self.supplimental_fields:
                    if not fld.null:
                        raise TypeError('Supplimental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(model._meta.object_name, fld.name))
                    if not fld.editable:
                        raise TypeError('Supplimental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(model._meta.object_name, fld.name))
            self.checked_fields = True
            self.fields = copy.deepcopy(fields)
        exclude_fields = []
        if obj:
            if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk).exists():
                exclude_fields = self.supplimental_fields
        else:
            if random.choice(self.p_as_sequence):  # if 0 or if 1
                exclude_fields = tuple(self.supplimental_fields)
        fields = tuple([f for f in list(self.fields) if f not in exclude_fields])
        return fields, exclude_fields
