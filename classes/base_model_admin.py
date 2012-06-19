from datetime import datetime
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from bhp_sync.actions import serialize
from bhp_crypto.actions import encrypt, decrypt
from bhp_crypto.classes import BaseEncryptedField


class BaseModelAdmin (admin.ModelAdmin):
    
    """Overide ModelAdmin to force username to be saved on add/change and other stuff""" 
    
    # override the default widget for encrypted fields
    #formfield_overrides = {
    #       EncryptedIdentityField: {'widget': forms.widgets.PasswordInput(render_value=True)},
    #       #EncryptedFirstnameField: {'widget': forms.widgets.PasswordInput(render_value=True)},
    ##       EncryptedLastnameField: {'widget': forms.widgets.PasswordInput(render_value=True)},
    #       }
    
    def __init__(self, *args, **kwargs):
        #add serialize action
        self.actions.append(serialize)
        self.actions.append(encrypt)    
        self.actions.append(decrypt)                            
                        
        super(BaseModelAdmin, self).__init__(*args, **kwargs)
    
    def save_model(self, request, obj, form, change):
        #add username
        if not change:
            obj.user_created = request.user.username
        
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()
        
        super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):

            result = super(BaseModelAdmin, self).add_view(request, form_url='', extra_context=None)
            
            # Catch named url from request.GET.get('next') and reverse 
            # resolve along with other GET parameters
            if request.GET.get('next'):
                kwargs={}
                for k in request.GET.iterkeys():
                    kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                del kwargs['next']
                try:
                    del kwargs['csrfmiddlewaretoken']                
                except:
                    pass    
                result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )

            return result
            
                

    def change_view(self, request, object_id, extra_context=None):

            result = super(BaseModelAdmin, self).change_view(request, object_id, extra_context)
            #Catch named url from request.GET.get('next') and reverse resolve along with other 
            # GET parameters
            if request.GET.get('next'):
                kwargs={}
                for k in request.GET.iterkeys():
                    kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                del kwargs['next']
                result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )

            return result

    def get_readonly_fields(self, request, obj = None):
        # make crypter fields readonly if no private key and in edit mode
        if obj: #In edit mode
            for field in obj._meta.fields:
                if isinstance(field, BaseEncryptedField):
                    if not field.crypter.private_key:
                        self.readonly_fields = (field.attname,) + self.readonly_fields 
        return self.readonly_fields
