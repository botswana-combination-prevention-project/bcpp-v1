from django.contrib import admin
from bhp_base_admin.mixin import SiteMixin
from bhp_supplimental_fields.models import Excluded


class BaseModelAdmin (SiteMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if 'supplimental_fields' in dir(self): 
            if self.form._meta.exclude:
                # record which instances were selected for excluded fields
                Excluded.objects.get_or_create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.form._meta.exclude)
            self.form._meta.exclude = None

    def get_form(self, request, obj=None, **kwargs):
        if 'supplimental_fields' in dir(self) and not request.method == 'POST':
            # we are using form._meta.exclude, so make sure it was not set in the form.Meta class
            if 'exclude' in dir(self.form.Meta):
                raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplimental_fields\'. See {0}.'.format(self.form))
            # always set to None first
            self.form._meta.exclude = None
            self.fields, exclude_supplimental_fields = self.supplimental_fields.update_fields(self.fields, self.form._meta.model, obj)
            if exclude_supplimental_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                self.form._meta.exclude = exclude_supplimental_fields
        return super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
