import logging
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class SiteMixin (object):

    def update_modified_stamp(self, request, obj, change):
        """Forces username to be saved on add/change and other stuff, called from save_model"""
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()

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

        http_response_redirect = super(SiteMixin, self).response_add(request, obj, post_url_continue)
        if '_savenext' in request.POST:
            pass
            #raise TypeError('Save next button is not currently in use. Click Save')
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
                    raise NoReverseMatch('response_add failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                    logger.warning('Warning: response_add failed to reverse \'{0}\' with kwargs {1}'.format(request.GET.get('next'), kwargs))
                    pass
                except:
                    raise
        return http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        """Redirects if keyword 'next' is a url name that can be reversed.

        See comment for response_add() above"""
        http_response_redirect = super(SiteMixin, self).response_add(request, obj, post_url_continue)
        if '_savenext' in request.POST:
            raise TypeError('Save next button is not currently in use. Click Save')
        if not '_addanother' in request.POST and not '_continue' in request.POST:
            # look for session variable "filtered" set in change_view
            if request.session.get('filtered', None):
                if 'next=' not in request.session.get('filtered'):
                    #result['Location'] = request.session['filtered']
                    http_response_redirect = HttpResponseRedirect(request.session['filtered'])
                    request.session['filtered'] = None
            # look for 'next' in URL querystring and reverse with kwargs for keyword string
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
                request.session['filtered'] = None
        return http_response_redirect

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ Saves the referer of the page to return to the filtered
        change_list after saving the page.

        from http://djangosnippets.org/snippets/2849/
        """
        result = super(SiteMixin, self).change_view(request, object_id, form_url, extra_context)
        # Look at the referer for a query string '^.*\?.*$'
        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            # We've got a query string, set the session value
            request.session['filtered'] = ref
        return result
