from django.core.exceptions import ValidationError
from bhp_content_type_map.models import ContentTypeMap


def is_visit_tracking_model(value):
    from bhp_visit_tracking.models import BaseVisitTracking
    if not isinstance(value, ContentTypeMap):
        raise ValidationError('Must be an instance of ContentTypeMap')
    if issubclass(value.model_class(), BaseVisitTracking):
        raise ValidationError('Select a model that is a subclass of BaseVistTracking')
