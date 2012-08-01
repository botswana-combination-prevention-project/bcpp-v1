from django.db.models import ForeignKey
from django.db.models import get_app, get_models
from bhp_visit_tracking.models import BaseVisitTracking


class VisitModelHelper(object):

    """ Help determine the name of the visit model foreign key and to return a queryset of that
    field for select/dropdowns (e.g. formfield_for_foreignkey in admin).

    I separated this code from BaseVisitModelAdmin because other models may wish to use it in their ModelAdmin
    which may not inheret from BaseVisitModelAdmin. For example, the lab requisition has a visit model 
    foreign key, needs to determine the visit field and get a queryset for the select/dropdown but its
    ModelAdmin class does not inheret from BaseVisitModelAdmin.

    """

    subject_identifier = None
    visit_code = None
    visit_instance = None
    model = None
    visit_model = None

    def set_visit_queryset(self, **kwargs):

        self.subject_identifier = kwargs.get('subject_identifier')
        self.visit_code = kwargs.get('visit_code')
        self.visit_instance = kwargs.get('visit_instance')
        return self.visit_model.objects.filter(appointment__registered_subject__subject_identifier=self.subject_identifier,
                                                    appointment__visit_definition__code=self.visit_code,
                                                    appointment__visit_instance=self.visit_instance,
                                                    )

    def get_visit_field(self, **kwargs):
        self.model = kwargs.get('model')
        self.visit_model = kwargs.get('visit_model')
        visit_fk = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        return visit_fk[0].name

    def get_visit_model(self, instance):
        """ given the instance of a model, return the visit model of its app """
        for model in get_models(get_app(instance._meta.app_label)):
            if isinstance(model(), BaseVisitTracking):
                return model
        raise TypeError('Unable to determine the visit model from instance {0} for app {1}'.format(instance._meta.model_name, instance._meta.app_label))
