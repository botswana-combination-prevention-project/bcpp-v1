import inspect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
from bhp_appointment.models.holiday import Holiday
from bhp_appointment.models.configuration import Configuration

class VisitManager(models.Manager):

    def get_by_natural_key(self, registered_subject, visit_definition, visit_instance):
        return self.get(registered_subject=registered_subject, visit_definition=visit_definition, visit_instance=visit_instance)
    
    def get_by_natural_key_with_dict(self, **kwargs):
        return self.get(**kwargs)
