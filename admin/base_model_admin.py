import logging
from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseModelAdmin (admin.ModelAdmin):

    """Overide ModelAdmin to force username to be saved on add/change and other stuff"""

    def save_model(self, request, obj, form, change):
        #add username
        if not change:
            obj.user_created = request.user.username

        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()

        super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects if keyword 'next' is a url name that can be reversed.

        Important:
        1. the value of next is NOT a url but a 'url name' where kwargs has
           the keyword/values needed to reverse the 'url name'.
        2. All keyword/values must be used for the reverse (except 'next' and 'csrfmiddlewaretoken').

        Example:
            In your urls.py a named url such as "survey_section_url":

                url(r'^(?P<section_name>household|mobile|statistics|administration)/(?P<survey>mpp\-year\-[0-9]{1}|mobile\-year\-[0-9]{1})/$',
                    'section_index', name="survey_section_url"),

            In your template, refer to this named url and provide the kwargs as hidden input tags.
                <form method="GET" action="/admin/mochudi_household/household/add/">
                    {% csrf_token %}
                    <input type='hidden' name="survey" value="{{selected_survey.survey_slug}}">
                    <input type='hidden' name="next" value="survey_section_url">
                    <input type="hidden" name="section_name" value="{{section_name}}">
                    <input type="submit" value="Create new household" class="default" />
                </form>
        """

        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                try:
                    kwargs = {}
                    for k, v in request.GET.iteritems():
                        kwargs[str(k)] = ''.join(unicode(i) for i in request.GET.get(k))
                        if not v:
                            if k in dir(obj):
                                try:
                                    kwargs[str(k)] = getattr(obj, k)
                                except:
                                    pass
                    del kwargs['next']
                    if 'csrfmiddlewaretoken' in kwargs.keys():
                        del kwargs['csrfmiddlewaretoken']
                    http_response_redirect = HttpResponseRedirect(reverse(request.GET.get('next'), kwargs=kwargs))
                except NoReverseMatch:
                    logger.warning('Warning: response_add failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                    pass
                except:
                    raise
        return http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        """Redirects if keyword 'next' is a url name that can be reversed.

        See comment for response_add() above"""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            if request.GET.get('next'):
                try:
                    kwargs = {}
                    for k in request.GET.iterkeys():
                        kwargs[str(k)] = ''.join(unicode(i) for i in request.GET.get(k))
                    del kwargs['next']
                    if 'csrfmiddlewaretoken' in kwargs.keys():
                        del kwargs['csrfmiddlewaretoken']
                    http_response_redirect = HttpResponseRedirect(reverse(request.GET.get('next'), kwargs=kwargs))
                except NoReverseMatch:
                    logger.warning('Warning: response_change failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                    pass
                except:
                    raise
        return http_response_redirect

    def add_view(self, request, *args, **kwargs):
        """ Deletes the session key, since we want the user to be directed to all listings
        after a save on a new object.

        from http://djangosnippets.org/snippets/2849/
        """
        result = super(BaseModelAdmin, self).add_view(request, *args, **kwargs)
        request.session['filtered'] = None
        return result
    """
    Used to redirect users back to their filtered list of locations if there were any
    """
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ Saves the referer of the page to return to the filtered
        change_list after saving the page.

        from http://djangosnippets.org/snippets/2849/
        """
        result = super(BaseModelAdmin, self).change_view(request, object_id, form_url, extra_context)
        # Look at the referer for a query string '^.*\?.*$'
        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            # We've got a query string, set the session value
            request.session['filtered'] = ref
        if '_save' in request.POST:
            """
            We only kick into action if we've saved and if
            there is a session key of 'filtered', then we
            delete the key.
            """
            try:
                if request.session['filtered'] is not None:
                    result['Location'] = request.session['filtered']
                    request.session['filtered'] = None
            except:
                pass
        return result
