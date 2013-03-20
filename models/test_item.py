from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.models import BaseListModel, TestManyToMany
from base_dispatch_sync_uuid_model import BaseDispatchSyncUuidModel
from test_container import TestContainer


class TestList(BaseListModel):
    class Meta:
        app_label = 'bhp_dispatch'


class TestItem(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestContainer)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (TestContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'


class TestItemTwo(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item = models.ForeignKey(TestItem)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'


class TestItemThree(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_two = models.ForeignKey(TestItemTwo)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item_two__test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'


class TestItemM2M(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_item_three = models.ForeignKey(TestItemThree)

    m2m = models.ManyToManyField(TestList)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return 'test_item_two__test_item__test_container__test_container_identifier'

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'
