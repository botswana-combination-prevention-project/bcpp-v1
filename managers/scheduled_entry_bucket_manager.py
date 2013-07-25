from django.db.models import get_model
from bhp_entry.managers import BaseEntryBucketManager
from bhp_content_type_map.models import ContentTypeMap
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition


class ScheduledEntryBucketManager(BaseEntryBucketManager):

    def get_by_natural_key(self, visit_instance, code, identity, first_name, dob, initials, registration_identifier, visit_definition, app_label, model):
        """Returns the instance using the natural key."""
        registered_subject = RegisteredSubject.objects.get(
            identity=identity,
            first_name=first_name,
            dob=dob,
            initials=initials,
            registration_identifier=registration_identifier
            )

        visit_definition = VisitDefinition.objects.get(code=code)
        Appointment = get_model('bhp_appointment', 'Appointment')
        appointment = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition=visit_definition,
            visit_instance=visit_instance
            )
        content_map_type = ContentTypeMap.objects.get(
            app_label=app_label,
            model=model
            )
        model = get_model('bhp_entry', 'Entry')
        entry = model.objects.get(
            content_map_type=content_map_type,
            visit_definition=visit_definition
            )
        return self.get(
            entry=entry,
            appointment=appointment
            )
