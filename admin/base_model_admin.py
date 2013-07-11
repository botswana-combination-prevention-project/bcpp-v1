from django.contrib import admin
from bhp_base_admin.mixin import SiteMixin
from bhp_supplemental_fields.models import Excluded


class BaseModelAdmin (SiteMixin, admin.ModelAdmin):

    instructions = 'Please complete the questions below.'
    required_instructions_add = 'Required questions are in bold. Additional questions may be required based on submitted data.'

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
        if 'supplemental_fields' in dir(self) or 'conditional_fields' in dir(self):
            if self.form._meta.exclude:
                # record which instances were selected for excluded fields, (see also the post_delete signal).
                Excluded.objects.get_or_create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.form._meta.exclude)
            self.form._meta.exclude = None

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        return super(BaseModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.instructions
        extra_context['required_instructions'] = self.required_instructions
        return super(BaseModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        """Overrides to check if conditional and supplemental fields have been defined in the admin class.

            * get_form is called once to render and again to save, e.g. on GET and then on POST.
            * Need to be sure that the same conditional and/or supplemental choice is given on GET and POST for both
              add and change.
        """
        if not request.method == 'POST':
            exclude_conditional_fields = None
            exclude_supplemental_fields = None
            if 'conditional_fields' in dir(self):
                # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
                if 'exclude' in dir(self.form.Meta):
                    raise AttributeError('The form.Meta attribute exclude cannot be used with \'conditional_fields\'. See {0}.'.format(self.form))
                # always set to None first
                self.form._meta.exclude = None
                self.fields, exclude_conditional_fields = self.conditional_fields.choose_fields(self.fields, self.form._meta.model, obj)
            if 'supplemental_fields' in dir(self):
                # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
                if 'exclude' in dir(self.form.Meta):
                    raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
                # always set to None first
                self.form._meta.exclude = None
                self.fields, exclude_supplemental_fields = self.supplemental_fields.choose_fields(self.fields, self.form._meta.model, obj)
            if exclude_conditional_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                self.form._meta.exclude = exclude_conditional_fields
            if exclude_supplemental_fields:
                # set exclude so that when the form is saved we use the same excluded fields from when the form was rendered
                if self.form._meta.exclude:
                    self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(exclude_supplemental_fields)))
                else:
                    self.form._meta.exclude = exclude_supplemental_fields
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        form = self.auto_number(form)
        return form

    def auto_number(self, form):
        WIDGET = 1
        auto_number = True
        if 'auto_number' in dir(form._meta):
            auto_number = form._meta.auto_number
        if auto_number:
            for index, fld in enumerate(form.base_fields.iteritems()):
                fld[WIDGET].label = '{0}. {1}'.format(index, fld[WIDGET].label)
        return form
