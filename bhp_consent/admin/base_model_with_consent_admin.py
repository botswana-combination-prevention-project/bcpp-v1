from django.db.models import ForeignKey
from bhp_crypto.admin import BaseCryptorModelAdmin
from bhp_registration.models import RegisteredSubject

# is this used??


class BaseModelWithConsentAdmin(BaseCryptorModelAdmin):
    """ NOT USED """

    """ For models with a key to consent"""
    def save_model(self, request, obj, form, change):
        #from bhp_appointment.models import Appointment
        if not change:
            consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name
            subject_identifier = self.form.__dict__['base_fields'][consent_fk_name].__dict__['_queryset'][0].subject_identifier
            rs = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
            obj.registered_subject = rs
            #if model is in a member of a schedule group, create appointments
            raise TypeError('appointments may not be created via admin. See bhp_appointment_helper')
            #Appointment.objects.create_appointments(
            #    registered_subject=obj.registered_subject,
            #    base_appt_datetime=datetime.today(),
            #    model_name=self.form._meta.model.__name__.lower())

        return super(BaseModelWithConsentAdmin, self).save_model(request, obj, form, change)

    #override, limit dropdown in add_view to id passed in the URL
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name
        if request.GET.get('subject_identifier'):
            if db_field.name == consent_fk_name:
                kwargs["queryset"] = self.consent_model.objects.filter(subject_identifier=request.GET.get('subject_identifier'))
        return super(BaseModelWithConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):

        super(BaseModelWithConsentAdmin, self).get_readonly_fields(request, obj)
        consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name
        if obj:  # In edit mode
            self.readonly_fields += (consent_fk_name,)
        return self.readonly_fields


# class BaseKeyToConsentModelAdmin(BaseModelWithConsentAdmin):
#     pass
