from datetime import datetime, date
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django_extensions.db.models import TimeStampedModel
from django.contrib import admin
from fields import HostnameCreationField, HostnameModificationField, MyUUIDField, OmangField
#from validators import datetime_not_before_study_start, datetime_not_future

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

"""
class BaseReportModel(MyBasicUuidModel):

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])

    class Meta:
        abstract = True   
"""


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
            obj.modified = datetime.today()
        
        return super(MyModelAdmin, self).save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):

            result = super(MyModelAdmin, self).add_view(request, form_url='', extra_context=None)

            """ Catch named url from request.GET.get('next') and reverse resolve along with other GET parameters"""
            if request.GET.get('next'):
                kwargs={}
                for k in request.GET.iterkeys():
                    kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                del kwargs['next']
                result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )

            return result
            
                

    def change_view(self, request, object_id, extra_context=None):

            result = super(MyModelAdmin, self).change_view(request, object_id, extra_context)

            """ Catch named url from request.GET.get('next') and reverse resolve along with other GET parameters"""
            if request.GET.get('next'):
                kwargs={}
                for k in request.GET.iterkeys():
                    kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                del kwargs['next']
                result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )

            return result
        


class MyStackedInline (admin.StackedInline):
    """Overide ModelAdmin to force username to be saved on add and change"""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
        obj.save()


class MyTabularInline (admin.TabularInline):
    """Overide ModelAdmin to force username to be saved on add and change"""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
        obj.save()
    

class ContentTypeMap(MyBasicModel):

    content_type = models.OneToOneField(ContentType)

    app_label = models.CharField(
        max_length = 50,
        )
    
    name = models.CharField(
        max_length = 50,
        unique = True,
        )
        
    model = models.CharField(
        max_length = 50,
        unique = True,        
        )
    
    def model_class(self):

        if not self.content_type.name == self.name:
            raise TypeError('ContentTypeMap is not in sync with ContentType for verbose_name %s' % self.name) 
        if not self.content_type.model == self.model:
            raise TypeError('ContentTypeMap is not in sync with ContentType for model %s' % self.model)
        
        return self.content_type.model_class()
    
    def __unicode__(self):
        return unicode(self.content_type)        
    class Meta:
        app_label = 'bhp_common'



    


