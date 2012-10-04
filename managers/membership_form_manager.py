from django.db import models


class MembershipFormManager(models.Manager):

    def codes_for_category(self, membership_form_category):
        """ Lists visit codes for this membership form category."""
        VisitDefinition = models.get_model('bhp_visit', 'visitdefinition')
        membership_forms = super(MembershipFormManager, self).filter(category=membership_form_category)
        visit_definition_codes = set()
        for membership_form in membership_forms:
            for visit_definition in VisitDefinition.objects.filter(schedule_group__membership_form=membership_form):
                visit_definition_codes.add(visit_definition.code)
        return list(visit_definition_codes)
