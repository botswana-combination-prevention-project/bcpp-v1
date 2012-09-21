from bhp_visit.models import VisitDefinition, ScheduleGroup


class VisitDefinitionHelper(object):

    @classmethod
    def list_all_for_model(self, registered_subject, model_name):
        """ Lists all visit_definitions for which appointments would be created or updated for this model_name"""
        if ScheduleGroup.objects.filter(membership_form__content_type_map__model=model_name):
            # get list of visits for scheduled group containing this model
            visit_definitions = VisitDefinition.objects.filter(
                schedule_group=ScheduleGroup.objects.get(membership_form__content_type_map__model=model_name))
        else:
            visit_definitions = []
        return visit_definitions
