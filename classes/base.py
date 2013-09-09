import copy
import random
from bhp_supplemental_fields.models import Excluded


class Base(object):
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

    def __init__(self, optional_fields, optional_field_label='optional_fields', **criteria):
        if not isinstance(optional_fields, tuple):
            raise AttributeError('Attribute \'{0}\' must be a tuple of field names. Got {0}'.format(optional_field_label))
        self._optional_fields = optional_fields
        self._original_fields = None
        self._are_fields_verified = False

    def choose_fields(self, fields, model, obj):
        """Chooses and returns tuples of fields and exclude_fields.

            * \'new_fields\' to include in ModelAdmin \'fields\' and;
            * \'exclude_fields\' for form._meta's \'exclude\' using random.choice and the probablility \'p\';
            * called from base_model_admin.get_form()
        """
        self._verify_fields(fields, model)
        exclude_fields = self._get_exclude_fields(obj)
        fields = self._get_updated_fields(exclude_fields)
        return fields, exclude_fields

    def _get_optional_fields(self):
        """Returns a list of field names that might be excluded from the ModelAdmin fields tuple."""
        return self._optional_fields

    def _set_original_fields(self, fields):
        """Save the original fields tuple as it is configured in the initial instance of the ModelAdmin."""
        self._original_fields = copy.deepcopy(fields)

    def _get_original_fields(self):
        return self._original_fields

    def _get_p_as_sequence(self):
        """Converts p to a list of 0s and 1s where 1s will include the fields.

        The default, 1, is to exclude the fields from the \'fields\' list.
        If p=0.1, the list will be 900 1s and 100 0s where the fields will be excluded
        from the list approximately 900 out of 1000 times.
        """
        return ([0] * int(1000 * self._p)) + ([1] * int(1000 - (1000 * self._p)))

    def _get_updated_fields(self, exclude_fields):
        """Sets and returns the fields list based on the original fields list less exclude fields (which may be [])."""
        return tuple([f for f in list(self._get_original_fields()) if f not in exclude_fields])

    def _get_exclude_fields(self, obj):
        """Sets and returns a list of fields to exclude from the original fields list.

        The return value is either an empty list or the list of optional_fields.

        Override this method to change how the choice is made between returning [] and optional_fields.
        """
        exclude_fields = []
        if obj:
            exclude_fields = self._stored_choice(exclude_fields, obj)
        else:
            exclude_fields = self._choice(exclude_fields)
        return exclude_fields

    def _choice(self, exclude_fields):
        if random.choice(self._get_p_as_sequence()):  # either 0 or 1
            exclude_fields = tuple(self._get_optional_fields())
        return exclude_fields

    def _stored_choice(self, exclude_fields, obj):
        if obj:
            raise AttributeError('Attribute \'obj\' cannot be None.')
        # you are editing, lookup the choice that was used to create obj.
        # Instances are only logged if exclude fields is not null
        # Instances are logged in :func:`base_model_admin.save_model`
        if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk).exists():
            exclude_fields = self._get_optional_fields()
        return exclude_fields

    def _verify_fields(self, fields, model):
        """Verifies all optional_fields exist in fields and keeps a unaltered copy of fields.

            * only runs once per instance.
            * does some error checking, e.g. form.Meta.exclude not set, field is editable an nullable
            * can work with \'required\' fields where null=True, blank=False.
        """
        if not self._are_fields_verified:
            # any field listed in supplimentatl_fields must be in fields
            for optional_field in self._get_optional_fields():
                if optional_field not in fields:
                    raise AttributeError('Supplemental field \'{0}\' must be listed in fields.'.format(optional_field))
            # optional_fields must be nullable and editable
            for fld in model._meta.fields:
                if fld.name in self._get_optional_fields():
                    if not fld.null:
                        raise TypeError('Supplemental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(model._meta.object_name, fld.name))
                    if not fld.editable:
                        raise TypeError('Supplemental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(model._meta.object_name, fld.name))
            # save the original ModelAdmin field list with this instance before it is altered
            self._set_original_fields(fields)
            # set to True so this code is not run again for this instance
            self._are_fields_verified = True
        return self._are_fields_verified
