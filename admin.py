from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import IssueTrackerHistory , IssueTracker
from models import MyModelAdmin

class IssueTrackerHistoryInline(admin.TabularInline):
    model = IssueTrackerHistory
    extra=1

class IssueTrackerAdmin (MyModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user_created = request.user
        obj.user_modified = request.user.username
        if not change:
            obj.item_uuid = request.GET.get('u')
            obj.item_id = request.GET.get('i')
            obj.item_type = request.GET.get('t')
            obj.item_app = request.GET.get('app')            
        obj.save()
    
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('item_uuid','item_id','item_type',) + self.readonly_fields
        else:
            return ('item_uuid','item_id','item_type',) + self.readonly_fields  

    def response_add(self, request, obj, post_url_continue='../%s/'):

        my_post_url='/%s/%s/%s/' % (request.GET.get('app'), request.GET.get('t'),request.GET.get('u'))
        
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = my_post_url
            else:
                post_url = '../../'
            return HttpResponseRedirect(post_url) 
    inlines=[IssueTrackerHistoryInline,]
admin.site.register(IssueTracker, IssueTrackerAdmin)
