from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
try:
    from bhp_sync.actions import serialize
except ImportError:
    pass


class BaseModelAdmin (admin.ModelAdmin):
    
    """Overide ModelAdmin to force username to be saved on add/change and other stuff""" 
    def __init__(self, *args, **kwargs):
        #add serialize action
        try:
            self.actions.append(serialize)
        except:
            pass                                  
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

    #    def get_readonly_fields(self, request, obj = None):
    #        # make crypter fields readonly if no private key and in edit mode
    #        if obj: #In edit mode
    #            for field in obj._meta.fields:
    #                if isinstance(field, BaseEncryptedField):
    #                    if not field.crypter.private_key and field.attname not in self.readonly_fields:
    #                        self.readonly_fields = (field.attname,) + self.readonly_fields 
    #        return self.readonly_fields
