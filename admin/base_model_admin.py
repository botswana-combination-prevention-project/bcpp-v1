from django.contrib import admin
from bhp_base_admin.mixin import SiteMixin
from bhp_supplemental_fields.models import Excluded


class BaseModelAdmin (SiteMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if 'supplemental_fields' in dir(self):
            if self.form._meta.exclude:
                # record which instances were selected for excluded fields, (see also the post_delete signal).
                Excluded.objects.get_or_create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.form._meta.exclude)
            self.form._meta.exclude = None

    def get_form(self, request, obj=None, **kwargs):
        """Overrides to check if supplemental fields have been defined in the admin class.

            * get_form is called once to render and again to save, e.g. on GET and then on POST.
            * Need to be sure that the same random choice is given on GET and POST for both
              add and change. Also, need to be sure the same random choice on 'add' is
              given for 'change'.
        """
        # do nothing if this is a POST
        if 'supplemental_fields' in dir(self) and not request.method == 'POST':
            # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
            if 'exclude' in dir(self.form.Meta):
                raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
            # always set to None first
            self.form._meta.exclude = None
            self.fields, exclude_supplemental_fields = self.supplemental_fields.choose_fields(self.fields, self.form._meta.model, obj)
            if exclude_supplemental_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                self.form._meta.exclude = exclude_supplemental_fields
        return super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
