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


class TestItemBypassForEdit(BaseDispatchSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    test_container = models.ForeignKey(TestContainer)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    f1 = models.CharField(max_length=35)
    f2 = models.CharField(max_length=35)
    f3 = models.CharField(max_length=35)
    f4 = models.CharField(max_length=35)

    comment = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.test_item_identifier

    def bypass_for_edit_dispatched_as_item(self):
        # requery myself
        obj = self.__class__.objects.get(pk=self.pk)
        #dont allow values in these fields to change if dispatched (means only f1, f2 can change)
        may_not_change = [(k, v) for k, v in obj.__dict__.iteritems() if k not in ['f1', 'f2']]
        for k, v in may_not_change:
            if k[0] != '_':
                if getattr(self, k) != v:
                    print 'cannot bypass, failed on field {0}'.format(k)
                    return False
        return True

    def is_dispatch_container_model(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (TestContainer, 'test_container__test_container_identifier')

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bhp_dispatch'
