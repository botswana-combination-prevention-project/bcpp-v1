from random import choice
from django.contrib import admin
from bhp_base_admin.mixin import SiteMixin


class BaseModelAdmin (SiteMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        if 'Meta' in dir(self.form) and 'randomise' in dir(self.form.Meta):#make sure the field is nullable or has a default value if not nullable
            for random_element in self.form.Meta.randomise:
                if self.form.base_fields[random_element[0]].required:
                    #need both null=True and blank=True in field declaration in model for field.required to be false
                    raise TypeError('Randomization field \'{0}\' cannot be a required field.'.format(random_element[0]))
                #rand_num = random.randint(0, 1)
                rand_num = choice(random_element[2])
                if random_element[0] in self.fields and rand_num == 0:#remove field
                    self.fields.remove(random_element[0])
                elif random_element[0] not in self.fields and rand_num == 1:#add field
                    self.fields.insert(random_element[1]-1,random_element[0])
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        return form