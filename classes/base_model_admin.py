from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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

    def response_add(self, request, obj, post_url_continue=None):
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                try:
                    kwargs = {}
                    for k in request.GET.iterkeys():
                        kwargs[str(k)] = ''.join(unicode(i) for i in request.GET.get(k))
                    del kwargs['next']
                    http_response_redirect = HttpResponseRedirect(reverse(request.GET.get('next'), kwargs=kwargs))
                except:
                    pass
        return http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                try:
                    kwargs = {}
                    for k in request.GET.iterkeys():
                        kwargs[str(k)] = ''.join(unicode(i) for i in request.GET.get(k))
                    del kwargs['next']
                    http_response_redirect = HttpResponseRedirect(reverse(request.GET.get('next'), kwargs=kwargs))
                except:
                    pass
        return http_response_redirect
