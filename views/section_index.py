import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bcpp.classes import SearchByWord


@login_required
def section_index(request, **kwargs):

    section_name = kwargs.get('section_name')
    search_name = kwargs.get('search_name')
    template = 'section_%s.html' % (section_name)
    if search_name is not None:
        """ get a top result list"""
        pass
    app_list = [app for app in settings.INSTALLED_APPS if re.search('^{app_name}'.format(app_name=settings.APP_NAME), app)]
    bhp_app_list = [app for app in settings.INSTALLED_APPS if re.search('^bhp', app)]
    search_by_word = SearchByWord()
    page = request.GET.get('page', '1')
    search_results = search_by_word.get_most_recent(search_name, page)
    return render_to_response(template, {
        'selected': section_name,
        'section_name': section_name,
        'search_name': search_name,
        'search_result': search_results,
        'top_result_include_file': "%s_include.html" % (search_name),
        'database': settings.DATABASES,
        'app_list': app_list,
        'app_name': settings.APP_NAME,
        'bhp_app_list': bhp_app_list,
    }, context_instance=RequestContext(request))
