from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from bhp_sync.actions import serialize


class MyModelAdmin (admin.ModelAdmin):
    
    """Overide ModelAdmin to force username to be saved on add and change""" 
    
    def __init__(self, *args, **kwargs):
        
        self.actions.append(serialize)
                            
        super(MyModelAdmin, self).__init__(*args, **kwargs)
    
    
    def save_model(self, request, obj, form, change):
        
        if not change:
            obj.user_created = request.user.username
        
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()
        
        super(MyModelAdmin, self).save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):

            result = super(MyModelAdmin, self).add_view(request, form_url='', extra_context=None)

            """ Catch named url from request.GET.get('next') and reverse resolve along with other GET parameters"""
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

            result = super(MyModelAdmin, self).change_view(request, object_id, extra_context)

            """ Catch named url from request.GET.get('next') and reverse resolve along with other GET parameters"""
            if request.GET.get('next'):
                kwargs={}
                for k in request.GET.iterkeys():
                    kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                del kwargs['next']
                #del kwargs['csrfmiddlewaretoken']
                result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )

            return result

