from django.db import models
from audit_trail.audit import AuditTrail
from bhp_sync.models import BaseSyncUuidModel


class TestItem(BaseSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    history = AuditTrail()

    class Meta:
        app_label = 'bhp_dispatch'
