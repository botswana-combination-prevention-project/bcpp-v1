from django.db import models
from audit_trail.audit import AuditTrail
from bhp_sync.models import BaseSyncUuidModel
from bhp_content_type_map.models import ContentTypeMap
from consent_catalogue import ConsentCatalogue


class AttachedModel(BaseSyncUuidModel):

    consent_catalogue = models.ForeignKey(ConsentCatalogue)

    content_type_map = models.ForeignKey(ContentTypeMap)

    history = AuditTrail()

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_consent'
        unique_together = (('consent_catalogue', 'content_type_map'), )
