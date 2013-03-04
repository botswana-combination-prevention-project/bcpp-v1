from django.db import models
from test_many_to_many import TestManyToMany
from base_uuid_model import BaseUuidModel
from test_foreign_key import TestForeignKey


class TestModel(BaseUuidModel):

    name = models.CharField(max_length=10)

    test_foreign_key = models.ForeignKey(TestForeignKey)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    class Meta:
        app_label = 'bhp_base_model'
