from django.db import models
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django_extensions.db.models import TimeStampedModel
from django.contrib import admin
from fields import HostnameCreationField, HostnameModificationField, MyUUIDField
from bhp_common.choices import ISSUE_STATUS

class MyBasicModel(TimeStampedModel):
    """
    Base model class for all models. Adds created and modified values for user, date and hostname (computer)
    """
    user_created = models.CharField(max_length=250, editable=False, default="")
    user_modified = models.CharField(max_length=250, editable=False, default="")
    hostname_created = HostnameCreationField()
    hostname_modified = HostnameModificationField()
    #version = models.CharField(max_length=10, editable=False, default='1.0')

    class Meta:
        abstract = True


class MyBasicUuidModel(MyBasicModel):
    """
    Base model class for all models that are populated in the field (decentralized environment). 
    Note that field "id" is an UUID and not an INT.
    """
    id = MyUUIDField(primary_key=True)

    def distributed(self):
        return True

    class Meta:
        abstract = True

class MyBasicListModel(MyBasicModel):
    """Basic List Model. Not intended to be edited in the field (decentralized environment)"""
    name = models.CharField(max_length=250, unique=True)
    short_name = models.CharField(max_length=250, unique=True)
    display_index = models.IntegerField(unique=True)
    field_name = models.CharField(max_length=25, null=True, blank=True)
    version = models.CharField(max_length=35, editable=False, default='1.0')

    def distributed(self):
        return False

    class Meta:
        abstract = True
        ordering=['display_index']

    def __unicode__(self):
        return self.name
        
class MyBasicCodeListModel(MyBasicListModel):
    """Basic Code List Model. Not intended to be edited in the field (decentralized environment)"""
    code = models.CharField(max_length=25, unique=True)
                
    def __unicode__(self):
        return "%s: %s" % (self.code, self.name)

    class Meta:
        abstract = True


class MyAutoCompleteAdminModel(ForeignKeyAutocompleteAdmin):
    pass

class MyModelAdmin (MyAutoCompleteAdminModel):
    """Overide ModelAdmin to force username to be saved on add and change""" 
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
        obj.save()


class MyStackedInline (admin.StackedInline):
    """Overide ModelAdmin to force username to be saved on add and change"""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
        obj.save()

    


class IssueTracker(MyBasicUuidModel):

    item_uuid = models.CharField(
        editable=False,
        max_length=50)

    item_id = models.CharField(
        max_length=50)

    
    item_type = models.CharField(
        max_length=50,
        )

    item_app = models.CharField(
        editable=False,
        max_length=50,
        )

    item_datetime = models.DateTimeField()

    subject = models.CharField(
        verbose_name="Subject line",
        max_length=35,
        )

    rt_number = models.IntegerField(
        blank=True,
        null=True,
        )

    description = models.TextField(
        max_length=250,
        verbose_name="Description",
        )
    
    status = models.CharField(
        max_length=25,
        choices=ISSUE_STATUS,
        verbose_name="Status",
        )
    def get_absolute_url(self):
        return "/bhp_common/issuetracker/%s/" % self.id
        
    def __unicode__(self):
        return '[rt #%s] %s' % (self.rt_number, self.subject)

    class Meta:
        ordering = ['-item_datetime',]
        
class IssueTrackerHistory(MyBasicUuidModel):
   
    history = models.ForeignKey(IssueTracker)
    
    item_datetime = models.DateTimeField()
    
    description = models.TextField(
        max_length=250,
        verbose_name="Description",
        )

    


