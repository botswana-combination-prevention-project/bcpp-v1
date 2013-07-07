import copy
import random
from bhp_supplimental_fields.models import Excluded


class SupplimentalFields(object):
    """ Excludes fields on the fly based on a given probability.

        * p is the probability the field will appear on the form; that is, will NOT be excluded from the fields attribute tuple
        * Fields are removed from the fields attribute tuple of an admin class.
        * Excluded fields are added to the form._meta.exclude tuple so that it operates correctly with the :func:clean method.
        * if the forms Meta class exclude attribute already specifies fields to exclude, an error will occur.

        For example::
            # If p=0.1, the supplimental fields will appear 100/1000 times the admin add form is shown.
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
            raise AttributeError('Attribute \'supplimental_fields\' must be a tuple of field names. Got {0}'.format(supplimental_fields))
        if not p < 1:
            raise AttributeError('Probability \'p\' must be less than 1. Got {0}.'.format(p))
        if len(str(p)) > 5:
            raise AttributeError('Probability \'p\' many not have more than 3 decimal places. Got {0}.'.format(p))
        # a p of .9 means the fields will NOT be removed 9/10 times
        # convert p to a list of 0s and 1s where 1 means the fields are removed from the list
        # the sequence always has 1000 elements to allow for 3 decimal places in p
        self._supplimental_fields = supplimental_fields
        self._p = p
        self._original_fields = None
        self._are_fields_verified = False

    def choose_fields(self, fields, model, obj):
        """Chooses and returns tuples of fields and exclude_fields.

            * \'fields\' to include in ModelAdmin \'fields\' and;
            * \'exclude_fields\' for form._meta's \'exclude\' using random.choice and the probablility \'p\';
            * called from base_model_admin.get_form()
        """
        self._verify_fields(fields, model)
        exclude_fields = self._get_exclude_fields(obj)
        fields = self._get_fields(exclude_fields)
        return fields, exclude_fields

    def _get_supplimental_fields(self):
        return self._supplimental_fields

    def _get_p_as_sequence(self):
        """Converts p to a list of 0s and 1s where 1s will include the fields.

        The default, 1, is to exclude the fields from the \'fields\' list.
        If p=0.1, the list will be 900 1s and 100 0s where the fields will be excluded
        from the list approximately 900 out of 1000 times.
        """
        return ([0] * int(1000 * self._p)) + ([1] * int(1000 - (1000 * self._p)))

    def _get_fields(self, exclude_fields):
        """Sets and returns the fields list based on the original fields list less exclude fields (which may be [])."""
        return tuple([f for f in list(self._original_fields) if f not in exclude_fields])

    def _get_exclude_fields(self, obj):
        """Sets and returns a list of fields to exclude from the original fields list.

            \'exclude_fields\' can be:
                * None ([]): not chosen or is an existing object that was not chosen when created;
                * list of fields: if chosen by random.choice for new objects or, for existing object, was chosen when it was created
                """
        exclude_fields = []
        if obj:
            # you are editing, lookup the choice that was used to create obj.
            # Instances are only logged if exclude fields is not null
            # Instances are logged in :func:`base_model_admin.save_model`
            if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk).exists():
                exclude_fields = self._get_supplimental_fields()
        else:
            if random.choice(self._get_p_as_sequence()):  # either 0 or 1
                exclude_fields = tuple(self._get_supplimental_fields())
        return exclude_fields

    def _verify_fields(self, fields, model):
        """Verifies all supplimental_fields exist in fields and keeps a unaltered copy of fields.

            * only runs once per instance.
            * does some error checking, e.g. form.Meta.exclude not set, field is editable an nullable
            * can work with \'required\' fields where null=True, blank=False.
        """
        if not self._are_fields_verified:
            # any field listed in supplimentatl_fields must be in fields
            for supplimental_field in self._get_supplimental_fields():
                if supplimental_field not in fields:
                    raise AttributeError('Supplimental field \'{0}\' must be listed in fields.'.format(supplimental_field))
            # supplimental_fields must be nullable and editable
            for fld in model._meta.fields:
                if fld.name in self._get_supplimental_fields():
                    if not fld.null:
                        raise TypeError('Supplimental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(model._meta.object_name, fld.name))
                    if not fld.editable:
                        raise TypeError('Supplimental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(model._meta.object_name, fld.name))
            # save the original ModelAdmin field list with this instance before it is altered
            self._original_fields = copy.deepcopy(fields)
            # set to True so this code is not run again for this instance
            self._are_fields_verified = True
        return self._are_fields_verified
